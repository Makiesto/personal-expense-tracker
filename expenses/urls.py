from django.urls import path

from . import views

app_name = "expenses"
urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("<int:category_id>/detail/", views.detail, name="detail"),
    path("add/", views.add_expense, name="add"),
    path("<int:expense_id>/remove/", views.remove_expense, name="remove"),
]
