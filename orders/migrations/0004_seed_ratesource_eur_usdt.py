from django.db import migrations


def add_default_rate_source(apps, schema_editor):
    RateSource = apps.get_model("orders", "RateSource")
    if RateSource.objects.filter(name="ExchangeRate-API EUR/USD (proxy)").exists():
        return
    RateSource.objects.create(
        name="ExchangeRate-API EUR/USD (proxy)",
        pair="EUR_USDT",
        url="https://api.exchangerate-api.com/v4/latest/EUR",
        json_path="rates.USD",
        is_active=True,
    )


def remove_default_rate_source(apps, schema_editor):
    RateSource = apps.get_model("orders", "RateSource")
    RateSource.objects.filter(name="ExchangeRate-API EUR/USD (proxy)").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0003_ratesource_headers"),
    ]

    operations = [
        migrations.RunPython(add_default_rate_source, remove_default_rate_source),
    ]
