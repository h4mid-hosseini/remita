from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("orders/", include("orders.urls")),
    path("", RedirectView.as_view(pattern_name="orders:new", permanent=False)),
]
