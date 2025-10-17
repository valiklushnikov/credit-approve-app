from django.core.paginator import Paginator
from django.urls import reverse_lazy


from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from django.views.generic import TemplateView, ListView
from formtools.wizard.views import SessionWizardView
from django.db.models import Sum, Count

from . import forms
from . import filters
from .models import PredictionConfig, CreditApplication
from .common import TEMPLATES, FORMS

from ml.services import get_ensemble


class DashboardView(LoginRequiredMixin, TemplateView):
    """
        Головна панель управління для користувачів та адміністраторів.

        Для звичайних користувачів:
            - Показує загальну статистику по схваленим заявкам
            - Відображає загальну суму схвалених кредитів

        Для адміністраторів:
            - Список всіх заявок з фільтрацією
            - Управління режимом прогнозування
            - Зміна статусу заявок
            - Видалення заявок

        Attributes:
            template_name (str): Шлях до шаблону
            form_class (Form): Форма для зміни конфігурації
            success_url (str): URL для редіректу після успішних дій
    """
    template_name = "credits/index.html"
    form_class = forms.PredictionConfigForm
    success_url = reverse_lazy("credits:index")

    def get_config(self):
        """
            Отримує або створює конфігурацію прогнозування.

            Returns:
                PredictionConfig: Об'єкт конфігурації
        """
        config, _ = PredictionConfig.objects.get_or_create(id=1)
        return config

    def get_form(self):
        """
            Повертає форму конфігурації прогнозування.

            Returns:
                PredictionConfigForm: Форма з поточними налаштуваннями
        """
        config = self.get_config()
        if self.request.method == "POST":
            return self.form_class(self.request.POST, instance=config)
        return self.form_class(instance=config)

    def get_total_approved_orders(self):
        """
            Розраховує статистику по схваленим заявкам.

            Returns:
                dict: Словник з ключами 'total_credits' та 'total_amount'
        """
        return CreditApplication.objects.filter(prediction_result=True).aggregate(
            total_credits=Count("id"), total_amount=Sum("loan_amount")
        )

    def get_filtered_orders(self):
        """
            Отримує відфільтрований список заявок.

            Returns:
                QuerySet: Набір заявок згідно встановлених фільтрів
        """
        queryset = CreditApplication.objects.select_related("user")
        self.filterset = filters.OrderFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def post(self, request, *args, **kwargs):
        """
            Обробляє POST запити для оновлення конфігурації або статусу заявки.

            Обробляє два типи запитів:
            1. Зміна активного режиму прогнозування (active_mode)
            2. Оновлення статусу заявки (prediction_result)

            Args:
                request (HttpRequest): HTTP запит
                *args: Позиційні аргументи
                **kwargs: Іменовані аргументи

            Returns:
                HttpResponse: Редірект на попередню сторінку або рендер з помилками форми
        """
        if "active_mode" in request.POST:
            form = self.form_class(request.POST, instance=self.get_config())
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(
                    request.META.get("HTTP_REFERER", self.success_url)
                )
            else:
                return self.render_to_response(self.get_context_data(form=form))

        elif "prediction_result" in request.POST:
            order_id = request.POST.get("order_id")
            order = get_object_or_404(CreditApplication, id=order_id)
            form = forms.UpdateStatusForm(request.POST, instance=order)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(
                    request.META.get("HTTP_REFERER", self.success_url)
                )
            else:
                return self.render_to_response(self.get_context_data(update_form=form))

        return self.render_to_response(self.get_context_data())

    def get_paginated_orders(self):
        """
            Розбиває заявки на сторінки.

            Returns:
                Page: Об'єкт сторінки з заявками (по 10 на сторінці)
        """
        orders = self.get_filtered_orders()
        paginator = Paginator(orders, 10)
        page_number = self.request.GET.get("page")
        return paginator.get_page(page_number)

    def get_context_data(self, **kwargs):
        """
            Формує контекст для шаблону залежно від типу користувача.

            Для адміністраторів додає:
            - Конфігурацію прогнозування
            - Форми для оновлення
            - Список заявок з пагінацією
            - Фільтри

            Для звичайних користувачів додає:
            - Загальну кількість схвалених кредитів
            - Загальну суму схвалених кредитів

            Args:
                **kwargs: Додаткові аргументи для контексту

            Returns:
                dict: Словник з даними для шаблону
        """
        context = super().get_context_data(**kwargs)
        config = self.get_config()
        totals_approved = self.get_total_approved_orders()
        form = kwargs.get("form", self.get_form())
        paginated_orders = self.get_paginated_orders()
        params = self.request.GET.copy()

        if "page" in params:
            params.pop("page")

        if self.request.user.is_superuser:
            context.update(
                {
                    "config": config,
                    "form": form,
                    "update_form": forms.UpdateStatusForm(),
                    "total_orders": paginated_orders,
                    "filter": self.filterset,
                    "params": params.urlencode(),
                }
            )
        else:
            context.update(
                {
                    "total_credits": totals_approved["total_credits"],
                    "total_amount": totals_approved["total_amount"] if totals_approved["total_amount"] else 0,
                }
            )
        return context


class CreditWizard(LoginRequiredMixin, SessionWizardView):
    """
        Майстер покрокового заповнення кредитної заявки.

        Проводить користувача через 11 кроків (або 10 для режиму mode2)
        для збору всієї необхідної інформації про заявку на кредит.

        Після завершення:
            - Відправляє дані в ML модель для прогнозування
            - Зберігає заявку в базу даних
            - Показує результат прогнозування

        Attributes:
            form_list (list): Список форм для кожного кроку
    """
    form_list = FORMS

    def get_context_data(self, form, **kwargs):
        """
            Додає інформацію про прогрес виконання кроків до контексту.

            Args:
                form (Form): Поточна форма кроку
                **kwargs: Додаткові аргументи

            Returns:
                dict: Контекст з індексом кроку, загальною кількістю кроків та прогресом у відсотках
        """
        context = super().get_context_data(form=form, **kwargs)
        context.update(
            {
                "step_index": self.steps.step1,
                "steps_total": self.steps.count,
                "progress": int((self.steps.step1 / self.steps.count) * 100),
            }
        )
        return context

    def get_form_list(self):
        """
            Формує список форм залежно від активного режиму прогнозування.

            У режимі mode2 пропускається крок "Кредитна історія".

            Returns:
                dict: Словник форм для відображення
        """
        predict_mode = PredictionConfig.objects.get(id=1)
        form_list = dict(super().get_form_list())

        if predict_mode.active_mode == "mode2":
            form_list.pop("credit_history", None)
        return form_list

    def get_template_names(self):
        """
            Повертає шаблон для поточного кроку.

            Returns:
                list: Список з шляхом до шаблону
        """
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        """
            Обробляє завершення майстра після всіх кроків.

            Збирає дані з усіх форм, виконує прогнозування через ML модель,
            зберігає заявку та відображає результат.

            Args:
                form_list (list): Список заповнених форм
                **kwargs: Додаткові аргументи

            Returns:
                HttpResponse: Сторінка з результатом прогнозування
        """
        data = {}
        for form in form_list:
            data.update(form.cleaned_data)
        predict_mode = PredictionConfig.objects.get(id=1)
        predict = get_ensemble().predict(data, predict_mode.active_mode)
        CreditApplication.objects.create(
            user=self.request.user, prediction_result=bool(predict), **data
        )

        return render(
            self.request,
            "credits/stepper/steps/result.html",
            {"approved": predict},
        )


class DeleteOrderView(LoginRequiredMixin, View):
    """
       Представлення для видалення кредитної заявки.

       Дозволяє користувачам видаляти власні заявки,
       а адміністраторам - будь-які заявки.

       Methods:
           post: Обробляє POST запит на видалення
    """
    def post(self, request, *args, **kwargs):
        """
            Видаляє заявку з бази даних.

            Args:
                request (HttpRequest): HTTP запит
                *args: Позиційні аргументи
                **kwargs: Іменовані аргументи (містить order_id)

            Returns:
                HttpResponse: Редірект на попередню сторінку

            Raises:
                Http404: Якщо заявку не знайдено
        """
        order_id = kwargs.get("order_id")
        order = get_object_or_404(CreditApplication, id=order_id)
        if order.user != request.user and not request.user.is_superuser:
            messages.error(request, "You do not have permission to delete this order")
            return redirect(request.META.get("HTTP_REFERER", "/"))
        order.delete()
        return redirect(request.META.get("HTTP_REFERER", "/"))


class UserOrdersView(LoginRequiredMixin, ListView):
    """
        Представлення для перегляду заявок користувача.

        Показує список всіх заявок поточного користувача
        з пагінацією по 10 записів на сторінці.

        Attributes:
            model (Model): Модель CreditApplication
            template_name (str): Шаблон для відображення
            context_object_name (str): Назва змінної в контексті
            paginate_by (int): Кількість записів на сторінці
    """
    model = CreditApplication
    template_name = "credits/includes/orders_list.html"
    context_object_name = "orders"
    paginate_by = 10

    def get_queryset(self):
        """
            Отримує список заявок для поточного користувача.

            Returns:
                QuerySet: Набір заявок, що належать поточному користувачу
        """
        return CreditApplication.objects.filter(user=self.request.user)
