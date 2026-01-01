import json
import urllib.request
from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.dateparse import parse_date, parse_datetime

try:
    import jdatetime
except Exception:
    jdatetime = None
from .forms import OrderCreateForm, PartnerCreateForm
from .models import Order, RateSource
from .services import OrderCalculator


def order_create(request):
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            return redirect("orders:detail", pk=order.pk)
    else:
        form = OrderCreateForm()

    return render(request, "orders/order_form.html", {"form": form})


def partner_create(request):
    if request.method == "POST":
        form = PartnerCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("orders:new")
    else:
        form = PartnerCreateForm()

    return render(request, "orders/partner_form.html", {"form": form})


def _extract_json_path(payload, path):
    current = payload
    for key in path.split("."):
        if isinstance(current, list):
            if key == "latest":
                if not current:
                    return None
                current = current[-1]
                continue
            try:
                index = int(key)
            except ValueError:
                return None
            if index < 0:
                index = len(current) + index
            if index < 0 or index >= len(current):
                return None
            current = current[index]
            continue

        if not isinstance(current, dict) or key not in current:
            return None
        current = current[key]
    return current


def rate_suggestions(request):
    pair = request.GET.get("pair")
    if not pair:
        return JsonResponse({"items": []})

    sources = RateSource.objects.filter(pair=pair, is_active=True)
    items = []
    for source in sources:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            if source.headers_json:
                try:
                    extra_headers = json.loads(source.headers_json)
                    if isinstance(extra_headers, dict):
                        headers.update({str(k): str(v) for k, v in extra_headers.items()})
                except json.JSONDecodeError:
                    pass

            request = urllib.request.Request(source.url, headers=headers)
            with urllib.request.urlopen(request, timeout=10) as response:
                payload = json.loads(response.read().decode("utf-8"))
            value = _extract_json_path(payload, source.json_path)
            if value is None:
                continue
            items.append(
                {
                    "id": source.id,
                    "name": source.name,
                    "price": str(value),
                }
            )
        except Exception:
            continue

    return JsonResponse({"items": items})


def _parse_range(start_value, end_value):
    def _normalize_digits(value):
        if not value:
            return value
        return (
            value.replace("۰", "0")
            .replace("۱", "1")
            .replace("۲", "2")
            .replace("۳", "3")
            .replace("۴", "4")
            .replace("۵", "5")
            .replace("۶", "6")
            .replace("۷", "7")
            .replace("۸", "8")
            .replace("۹", "9")
        )

    def _parse_jalali(value):
        if not value or not jdatetime:
            return None
        normalized = _normalize_digits(value)
        try:
            jd = jdatetime.datetime.strptime(normalized, "%Y/%m/%d %H:%M")
            return jd.togregorian()
        except ValueError:
            return None

    start_value = _normalize_digits(start_value)
    end_value = _normalize_digits(end_value)

    start_dt = parse_datetime(start_value) if start_value else None
    end_dt = parse_datetime(end_value) if end_value else None

    if start_dt is None and start_value:
        start_dt = _parse_jalali(start_value)
    if end_dt is None and end_value:
        end_dt = _parse_jalali(end_value)

    if start_dt is None and start_value:
        start_date = parse_date(start_value)
        if start_date:
            start_dt = timezone.datetime.combine(start_date, timezone.datetime.min.time())

    if end_dt is None and end_value:
        end_date = parse_date(end_value)
        if end_date:
            end_dt = timezone.datetime.combine(end_date, timezone.datetime.min.time())

    if start_dt and timezone.is_naive(start_dt):
        start_dt = timezone.make_aware(start_dt)
    if end_dt and timezone.is_naive(end_dt):
        end_dt = timezone.make_aware(end_dt)

    return start_dt, end_dt


def order_list(request):
    start_value = request.GET.get("start")
    end_value = request.GET.get("end")
    start_dt, end_dt = _parse_range(start_value, end_value)

    orders = Order.objects.select_related("partner").order_by("-created_at")
    if start_dt:
        orders = orders.filter(created_at__gte=start_dt)
    if end_dt:
        orders = orders.filter(created_at__lt=end_dt + timezone.timedelta(days=1))

    rows = []
    totals = {
        "orders": 0,
        "customer_should_pay_usdt": Decimal("0"),
        "partner_usdt_amount": Decimal("0"),
        "profit_usdt": Decimal("0"),
    }

    for order in orders:
        calc = OrderCalculator.calculate(order)
        rows.append(
            {
                "order": order,
                "calc": calc,
            }
        )
        totals["orders"] += 1
        totals["customer_should_pay_usdt"] += calc["customer_should_pay_usdt"]
        totals["partner_usdt_amount"] += calc["partner_usdt_amount"]
        totals["profit_usdt"] += calc["profit_usdt"]

    return render(
        request,
        "orders/order_list.html",
        {
            "rows": rows,
            "totals": totals,
            "start": start_value or "",
            "end": end_value or "",
        },
    )


def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    calculations = OrderCalculator.calculate(order)
    return render(
        request,
        "orders/order_result.html",
        {"order": order, "calc": calculations},
    )
