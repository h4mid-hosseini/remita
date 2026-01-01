from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Partner",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "direction",
                    models.CharField(
                        choices=[("INCOMING", "Incoming"), ("OUTGOING", "Outgoing")],
                        max_length=10,
                    ),
                ),
                ("requested_eur", models.DecimalField(decimal_places=2, max_digits=18)),
                ("commission_percent", models.DecimalField(decimal_places=4, max_digits=9)),
                ("partner_commission_eur", models.DecimalField(decimal_places=2, max_digits=18)),
                ("eur_to_usdt", models.DecimalField(decimal_places=8, max_digits=18)),
                ("usdt_to_irt", models.DecimalField(decimal_places=2, max_digits=18)),
                (
                    "customer_payment_currency",
                    models.CharField(
                        choices=[("EUR", "EUR"), ("USDT", "USDT"), ("IRT", "IRT")],
                        max_length=4,
                    ),
                ),
                (
                    "customer_paid_amount",
                    models.DecimalField(blank=True, decimal_places=8, max_digits=20, null=True),
                ),
                (
                    "customer_paid_currency",
                    models.CharField(
                        blank=True,
                        choices=[("EUR", "EUR"), ("USDT", "USDT"), ("IRT", "IRT")],
                        max_length=4,
                        null=True,
                    ),
                ),
                (
                    "profit_currency",
                    models.CharField(choices=[("USDT", "USDT"), ("IRT", "IRT")], max_length=4),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "partner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="orders",
                        to="orders.partner",
                    ),
                ),
            ],
        ),
    ]
