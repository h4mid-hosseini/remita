from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("", views.order_list, name="list"),
    path("new/", views.order_create, name="new"),
    path("partners/new/", views.partner_create, name="partner_new"),
    path("rate-suggestions/", views.rate_suggestions, name="rate_suggestions"),
    path("<int:pk>/", views.order_detail, name="detail"),
]
