from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Order, Partner


class PartnerCreateForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "w-full"}),
        }


class OrderCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (
                f"{existing} w-full rounded border border-slate-300 px-3 py-2 text-sm"
            ).strip()
        if user is not None:
            self.fields["partner"].queryset = Partner.objects.filter(owner=user)

    class Meta:
        model = Order
        fields = [
            "direction",
            "requested_eur",
            "commission_percent",
            "partner_commission_eur",
            "eur_to_usdt",
            "usdt_to_irt",
            "partner",
            "customer_payment_currency",
            "customer_paid_amount",
            "customer_paid_currency",
            "profit_currency",
            "notes",
        ]
        widgets = {
            "direction": forms.Select(attrs={"class": "w-full"}),
            "customer_payment_currency": forms.Select(attrs={"class": "w-full"}),
            "customer_paid_currency": forms.Select(attrs={"class": "w-full"}),
            "profit_currency": forms.Select(attrs={"class": "w-full"}),
            "partner": forms.Select(attrs={"class": "w-full"}),
        }
        help_texts = {
            "commission_percent": _("Enter as a multiplier (0.05 for 5%)."),
        }
