# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Ticket, Review


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
