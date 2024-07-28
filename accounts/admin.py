from django.contrib import admin
from django.contrib.admin import register
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

# from accounts.forms import CustomUserCreationForm, CustomUserChangeForm


CustomUser = get_user_model()


@register(CustomUser)
class CustomUserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    model = CustomUser
    list_display = [
        "email",
        "username",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "is_superuser",
        "is_engineer",
        "is_editor",
        "is_approver",
    ]
    list_filter = ["is_active", "is_staff", "is_superuser", "is_engineer", "is_editor", "is_approver"]
    fieldsets = (
        *BaseUserAdmin.fieldsets,
        (
            'Helpdesk User Type',
            {
                'fields': (
                    'is_customer',
                    'is_engineer',
                )
            }
        ),
        (
            'Post User Type',
            {
                'fields': (
                    'is_contributor',
                    'is_editor',
                    'is_approver',
                )
            }
        )
    )
