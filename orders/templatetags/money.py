from decimal import Decimal, ROUND_HALF_UP
from django import template

register = template.Library()


@register.filter
def format_money(value, currency=None):
    if value is None or value == "":
        return ""

    amount = Decimal(value)
    if currency == "IRT":
        quant = Decimal("1")
    else:
        quant = Decimal("0.01")

    return f"{amount.quantize(quant, rounding=ROUND_HALF_UP):f}"
