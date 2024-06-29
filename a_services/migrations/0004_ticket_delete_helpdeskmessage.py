# Generated by Django 5.0.6 on 2024-06-27 00:25

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("a_services", "0003_helpdeskmessage_status"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Ticket",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ticket_number", models.UUIDField(default=uuid.uuid4)),
                ("title", models.CharField(max_length=100)),
                ("description", models.TextField()),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_accepted", models.DateTimeField(blank=True, null=True)),
                ("is_resolved", models.BooleanField(default=False)),
                ("date_resolved", models.DateTimeField(blank=True, null=True)),
                (
                    "ticket_status",
                    models.CharField(
                        choices=[
                            ("Active", "Active"),
                            ("Completed", "Completed"),
                            ("Pending", "Pending"),
                        ],
                        max_length=15,
                    ),
                ),
                (
                    "assigned_to",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="assigned_to",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="created_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="HelpdeskMessage",
        ),
    ]
