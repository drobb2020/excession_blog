# -*- coding: utf-8 -*-
from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Answer, Option, Profile, Question, Submission, Survey


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'image',
        'display_name',
        'fav_quote',
        'fav_quote_author',
        'bio',
        'social_website',
        'created_at',
        'updated_at',
    )
    list_filter = ('user', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'is_active',
        'creator',
        'created_at',
        'updated_at',
    )
    list_filter = ('is_active', 'creator', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'survey', 'prompt', 'created_at', 'updated_at')
    list_filter = ('survey', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'text', 'created_at', 'updated_at')
    list_filter = ('question', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'survey',
        'is_complete',
        'created_at',
        'updated_at',
    )
    list_filter = ('survey', 'is_complete', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'submission', 'option', 'created_at', 'updated_at')
    list_filter = ('submission', 'option', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
