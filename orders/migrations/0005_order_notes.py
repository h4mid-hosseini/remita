from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0004_seed_ratesource_eur_usdt"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="notes",
            field=models.TextField(blank=True),
        ),
    ]
