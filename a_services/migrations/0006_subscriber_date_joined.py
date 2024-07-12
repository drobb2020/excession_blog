# Generated by Django 5.0.6 on 2024-07-07 14:07

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("a_services", "0005_subscriber_emailtemplate"),
    ]

    operations = [
        migrations.AddField(
            model_name="subscriber",
            name="date_joined",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
