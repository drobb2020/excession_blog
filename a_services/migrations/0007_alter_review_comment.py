# Generated by Django 5.1.4 on 2025-01-05 13:08

import tinymce.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("a_services", "0006_subscriber_date_joined"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="comment",
            field=tinymce.models.HTMLField(),
        ),
    ]
