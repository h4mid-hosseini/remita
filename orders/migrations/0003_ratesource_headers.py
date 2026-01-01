from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0002_ratesource"),
    ]

    operations = [
        migrations.AddField(
            model_name="ratesource",
            name="headers_json",
            field=models.TextField(
                blank=True,
                help_text="Optional JSON headers, e.g. {\"Accept\":\"application/json\"}",
            ),
        ),
    ]
