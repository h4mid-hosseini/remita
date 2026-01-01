from datetime import datetime, date
from django import template
from django.utils import timezone, translation

try:
    import jdatetime
except Exception:
    jdatetime = None

register = template.Library()

PERSIAN_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")


def _to_persian_digits(value: str) -> str:
    return value.translate(PERSIAN_DIGITS)


@register.filter
def format_datetime(value):
    if value is None or value == "":
        return ""

    lang = translation.get_language() or "en"

    if isinstance(value, date) and not isinstance(value, datetime):
        dt_value = datetime.combine(value, datetime.min.time())
    else:
        dt_value = value

    if isinstance(dt_value, datetime):
        dt_value = timezone.localtime(dt_value)

    if lang.startswith("fa") and jdatetime:
        jd = jdatetime.datetime.fromgregorian(datetime=dt_value)
        formatted = jd.strftime("%Y/%m/%d %H:%M")
        return _to_persian_digits(formatted)

    return dt_value.strftime("%Y-%m-%d %H:%M")
