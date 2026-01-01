from django.db import models
from django.utils.translation import gettext_lazy as _


class Partner(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("Name"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Partner")
        verbose_name_plural = _("Partners")


class Order(models.Model):
    DIRECTION_INCOMING = "INCOMING"
    DIRECTION_OUTGOING = "OUTGOING"
    DIRECTION_CHOICES = [
        (DIRECTION_INCOMING, _("Incoming")),
        (DIRECTION_OUTGOING, _("Outgoing")),
    ]

    CURRENCY_EUR = "EUR"
    CURRENCY_USDT = "USDT"
    CURRENCY_IRT = "IRT"
    CURRENCY_CHOICES = [
        (CURRENCY_EUR, _("EUR")),
        (CURRENCY_USDT, _("USDT")),
        (CURRENCY_IRT, _("IRT")),
    ]

    PROFIT_USDT = "USDT"
    PROFIT_IRT = "IRT"
    PROFIT_CHOICES = [
        (PROFIT_USDT, _("USDT")),
        (PROFIT_IRT, _("IRT")),
    ]

    direction = models.CharField(max_length=10, choices=DIRECTION_CHOICES, verbose_name=_("Direction"))
    requested_eur = models.DecimalField(max_digits=18, decimal_places=2, verbose_name=_("Requested EUR"))
    commission_percent = models.DecimalField(max_digits=9, decimal_places=4, verbose_name=_("Commission percent"))
    partner_commission_eur = models.DecimalField(
        max_digits=18, decimal_places=2, verbose_name=_("Partner commission EUR")
    )
    eur_to_usdt = models.DecimalField(max_digits=18, decimal_places=8, verbose_name=_("EUR → USD rate"))
    usdt_to_irt = models.DecimalField(max_digits=18, decimal_places=2, verbose_name=_("USD → IRT rate"))
    partner = models.ForeignKey(
        Partner, on_delete=models.PROTECT, related_name="orders", verbose_name=_("Partner")
    )

    customer_payment_currency = models.CharField(
        max_length=4, choices=CURRENCY_CHOICES, verbose_name=_("Customer payment currency")
    )
    customer_paid_amount = models.DecimalField(
        max_digits=20, decimal_places=8, null=True, blank=True, verbose_name=_("Customer paid amount")
    )
    customer_paid_currency = models.CharField(
        max_length=4, choices=CURRENCY_CHOICES, null=True, blank=True, verbose_name=_("Customer paid currency")
    )
    profit_currency = models.CharField(max_length=4, choices=PROFIT_CHOICES, verbose_name=_("Profit currency"))

    notes = models.TextField(blank=True, verbose_name=_("Notes"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))

    def __str__(self):
        return f"Order {self.id} - {self.partner}"

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")


class RateSource(models.Model):
    PAIR_EUR_USDT = "EUR_USDT"
    PAIR_USDT_IRT = "USDT_IRT"
    PAIR_CHOICES = [
        (PAIR_EUR_USDT, _("EUR → USDT")),
        (PAIR_USDT_IRT, _("USDT → IRT")),
    ]

    name = models.CharField(max_length=200, verbose_name=_("Name"))
    pair = models.CharField(max_length=20, choices=PAIR_CHOICES, verbose_name=_("Pair"))
    url = models.URLField(verbose_name=_("URL"))
    json_path = models.CharField(
        max_length=500,
        help_text=_("Dot-separated path like currencies.USDT.IRT.price"),
        verbose_name=_("JSON path"),
    )
    headers_json = models.TextField(
        blank=True,
        help_text=_("Optional JSON headers, e.g. {\"Accept\":\"application/json\"}"),
        verbose_name=_("Headers JSON"),
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))

    def __str__(self):
        return f"{self.name} ({self.get_pair_display()})"

    class Meta:
        verbose_name = _("Rate source")
        verbose_name_plural = _("Rate sources")
