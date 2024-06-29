from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager
from tinymce import models as tinymce_models
from django.template.defaultfilters import slugify

User = get_user_model()


def post_directory_path(instance, filename):
    return "posts/{0}".format(filename)


class Post(models.Model):
    OPTIONS = (
        ("draft", "Draft"),
        ("reviewed", "Reviewed"),
        ("published", "Published"),
        ("updated", "Updated"),
    )
    title = models.CharField(max_length=250)
    subtitle = tinymce_models.HTMLField()
    slug = models.SlugField(max_length=250, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_author")
    content = tinymce_models.HTMLField()
    post_image = models.ImageField(upload_to=post_directory_path, default="posts/default.jpg", null=True, blank=True)
    published_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=OPTIONS, default="draft")
    is_featured = models.BooleanField(default=False)
    tags = TaggableManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ("-created_at",)
