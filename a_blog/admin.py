from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "get_tags", "created_at")
    search_fields = ("title", "status")
    prepopulated_fields = {
        "slug": ("title",)
    }
    list_filter = ("author", "status", "created_at")

    def get_tags(self, obj):
        return ", ".join(o.name for o in obj.tags.all())
