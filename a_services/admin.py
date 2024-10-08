# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import EmailTemplate, Review, Subscriber, Ticket


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'review_title',
        'created_at',
        'approved',
    )
    list_filter = ('user', 'created_at', 'approved')
    date_hierarchy = 'created_at'


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'created_by',
        'assigned_to',
    )
    list_filter = ('title', 'created_by', 'is_resolved')
    date_hierarchy = 'date_created'


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email'
    )
    list_filter = ('name', 'email')
    date_hierarchy = 'date_joined'


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = (
        'subject',
    )
    list_filter = ('subject', 'message')
