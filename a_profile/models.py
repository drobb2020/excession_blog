from django.contrib.auth import get_user_model
from django.db import models
from django.templatetags.static import static

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="avatars/", null=True, blank=True)
    display_name = models.CharField(max_length=200, null=True, blank=True)
    fav_quote = models.CharField(max_length=250, blank=True)
    fav_quote_author = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    social_website = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)

    @property
    def name(self):
        if self.display_name:
            name = self.display_name
        else:
            name = self.user.username
        return name

    @property
    def avatar(self):
        try:
            avatar = self.image.url
        except Exception:
            avatar = static('images/avatar.png')
        return avatar
