# -*- coding: utf-8 -*-
from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Choice, Profile, Question


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "display_name",
        "fav_quote",
        "fav_quote_author",
        "bio",
        "social_website",
        "created_at",
        "updated_at",
    )
    list_filter = ("user", "created_at", "updated_at")
    date_hierarchy = "created_at"


@admin.register(Choice)
class ChoiceAdmin(ModelAdmin):
    list_display = (
        "choice_text",
        "question",
        "votes",
    )
    list_filter = ("choice_text", "created_at", "updated_at", "votes")
    search_fields = ("question",)
    date_hierarchy = "created_at"


@admin.register(Question)
class QuestionAdmin(ModelAdmin):
    list_display = (
        "question_text",
        "created_at",
    )
    list_filter = ("question_text", "created_at", "updated_at")
    search_fields = ("question_text",)
    date_hierarchy = "created_at"
