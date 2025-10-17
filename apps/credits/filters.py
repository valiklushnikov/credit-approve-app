import django_filters
from django.utils import timezone
from datetime import timedelta
from django import forms
from .models import CreditApplication


class OrderFilter(django_filters.FilterSet):
    """
        Фільтр для кредитних заявок за періодами часу.

        Дозволяє фільтрувати заявки за різними часовими періодами:
        всі, сьогодні, вчора, тиждень, місяць, минулий місяць, рік.

        Поля:
            period: Вибір часового періоду для фільтрації
    """
    PERIOD_CHOICES = [
        ("all", "All"),
        ("today", "Today"),
        ("yesterday", "Yesterday"),
        ("week", "Week"),
        ("month", "This month"),
        ("last_month", "Last month"),
        ("year", "This year"),
    ]

    period = django_filters.ChoiceFilter(
        label="Period",
        choices=PERIOD_CHOICES,
        method="filter_by_period",
        widget=forms.Select(
            attrs={
                "class": "form-control text-center",
                "id": "form-active-mode",
                "placeholder": " ",
            }
        ),
    )

    class Meta:
        model = CreditApplication
        fields = ["period"]

    def filter_by_period(self, queryset, name, value):
        """
            Фільтрує queryset за вибраним часовим періодом.

            Args:
                queryset: Набір об'єктів для фільтрації
                name: Назва поля фільтру
                value: Значення періоду (today, yesterday, week, month, last_month, year, all)

            Returns:
                QuerySet: Відфільтрований набір кредитних заявок
        """
        now = timezone.now()

        if value == "today":
            return queryset.filter(created_at__date=now.date())
        elif value == "yesterday":
            return queryset.filter(created_at__date=(now - timedelta(days=1)).date())
        elif value == "week":
            start_of_week = now - timedelta(days=now.weekday())
            end_of_week = start_of_week + timedelta(days=6)
            return queryset.filter(
                created_at__date__gte=start_of_week.date(),
                created_at__date__lte=end_of_week.date(),
            )
        elif value == "month":
            return queryset.filter(
                created_at__month=now.month, created_at__year=now.year
            )
        elif value == "last_month":
            return queryset.filter(
                created_at__month=now.month - 1, created_at__year=now.year
            )
        elif value == "year":
            return queryset.filter(created_at__year=now.year)
        return queryset
