from django import forms
from django.contrib.auth import get_user_model

from a_profile.models import Profile

User = get_user_model()


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ["user"]
        widgets = {
            "image": forms.FileInput(),
            "display_name": forms.TextInput(attrs={"placeholder": "Add display name"}),
            "fav_quote": forms.TextInput(
                attrs={"placeholder": "Add your favorite quote"}
            ),
            "fav_quote_author": forms.TextInput(
                attrs={"placeholder": "Add your favorite quote Author"}
            ),
            "bio": forms.Textarea(attrs={"rows": 3, "placeholder": "Add information"}),
            "social_website": forms.TextInput(
                attrs={"placeholder": "Your portfolio website"}
            ),
        }


class EmailForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["email"]
