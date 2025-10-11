from django.urls import path
from . import views

app_name = "credits"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="home"),
    path(
        "make_predict/",
        views.CreditWizard.as_view(views.CreditWizard.form_list),
        name="make_predict",
    ),
    path(
        "orders/<int:order_id>/delete/",
        views.DeleteOrderView.as_view(),
        name="delete_order",
    ),
    path("user_orders/", views.UserOrdersView.as_view(), name="user_orders"),
]
