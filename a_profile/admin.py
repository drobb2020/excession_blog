# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
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
