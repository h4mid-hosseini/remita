from django.contrib import admin
from .models import Partner, Order, RateSource


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "direction", "partner", "requested_eur", "created_at")
    list_filter = ("direction", "partner")
    search_fields = ("id",)


@admin.register(RateSource)
class RateSourceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "pair", "is_active")
    list_filter = ("pair", "is_active")
    search_fields = ("name", "url")
