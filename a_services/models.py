import uuid

from django.contrib.auth import get_user_model
from django.db import models
from tinymce import models as tinymce_models

from a_profile.models import Profile

User = get_user_model()


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="review")
    email = models.EmailField(max_length=100)
    review_title = models.CharField(max_length=150)
    comment = models.TextField(max_length=1250)
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}"


class Ticket(models.Model):
    STATUS_CHOICES = (
        ("Active", "Active"),
        ("Completed", "Completed"),
        ("Pending", "Pending"),
    )

    ticket_number = models.UUIDField(default=uuid.uuid4)
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_by"
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="assigned_to",
        blank=True,
        null=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_accepted = models.DateTimeField(blank=True, null=True)
    # first_technical_contact = models.DateTimeField(blank=True, null=True)
    # suggested_action = models.CharField(max_length=255, blank=True)
    # resolution = models.TextField(blank=True)
    is_resolved = models.BooleanField(default=False)
    date_resolved = models.DateTimeField(blank=True, null=True)
    # kb_created = models.BooleanField(default=False)
    ticket_status = models.CharField(max_length=15, choices=STATUS_CHOICES)

    def __str__(self):
        return self.title


class Subscriber(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"


class EmailTemplate(models.Model):
    subject = models.CharField(max_length=255)
    message = tinymce_models.HTMLField()
    recipients = models.ManyToManyField(Subscriber)

    def __str__(self):
        return self.subject
