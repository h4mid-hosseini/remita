from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="RateSource",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                (
                    "pair",
                    models.CharField(
                        choices=[("EUR_USDT", "EUR → USDT"), ("USDT_IRT", "USDT → IRT")],
                        max_length=20,
                    ),
                ),
                ("url", models.URLField()),
                (
                    "json_path",
                    models.CharField(
                        help_text="Dot-separated path like currencies.USDT.IRT.price",
                        max_length=500,
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
            ],
        ),
    ]
