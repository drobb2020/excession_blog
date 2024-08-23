from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import RangeDateFilter
from unfold.contrib.import_export.forms import ExportForm, ImportForm

from .models import Comment, Post


@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = (
        "post",
        "name",
        "email",
        "created_at",
        "status",
    )
    list_filter = ("post", "created_at", "updated_at", "status")
    search_fields = ("name",)
    date_hierarchy = "created_at"


@admin.register(Post)
class PostAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("title", "author", "status", "get_tags", "created_at")
    actions = ["post_review_action", "post_published_action"]
    import_form_class = ImportForm
    export_form_class = ExportForm
    search_fields = ("title", "status")
    prepopulated_fields = {"slug": ("title",)}
    list_filter = [
        "author",
        "status",
        ("created_at", RangeDateFilter),
        ("updated_at", RangeDateFilter),
    ]
    list_filter_submit = True

    def get_tags(self, obj):
        return ", ".join(o.name for o in obj.tags.all())

    @admin.action(description="Mark selected posts as under review")
    def post_review_action(self, request, queryset):
        posts_review = queryset.exclude(status=Post.PostStatus.REVIEW)
        posts = list(posts_review)

        posts_review.update(status=Post.PostStatus.REVIEW)

        # email User
        for post in posts:
            user = post.author
            user.email_user(
                "Your post is being reviewed",
                f"Dear {user.username}, \n\nYour post with ID {post.id} is being reviewed, and will be published after the review is complete. Please remember that all posts are subject to review, and must meet the standards listed in the Member Post Agreement found in the footer of the website.",
                "djadmin@exmple.com",
                fail_silently=False,
            )

        self.message_user(
            request,
            "Selected posts have been marked as review and author's have been notified.",
        )

    @admin.action(description="Mark selected posts as published")
    def post_published_action(self, request, queryset):
        posts_published = queryset.exclude(status=Post.PostStatus.PUBLISHED)
        posts = list(posts_published)

        posts_published.update(status=Post.PostStatus.PUBLISHED)

        # email User
        for post in posts:
            user = post.author
            user.email_user(
                "Your post has been published",
                f"Dear {user.username}, \n\nYour post with ID {post.id} has been published as it meets the standards listed in the Member Post Agreement found in the footer of the website. Good work, please keep posting new content.",
                "djadmin@exmple.com",
                fail_silently=False,
            )

        self.message_user(
            request,
            "Selected posts have been marked as published and author's have been notified.",
        )
