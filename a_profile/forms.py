from django import forms
from django.contrib.auth import get_user_model

from a_profile.models import Option, Profile, Question, Survey

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
                attrs={"placeholder": "Add the author of your favorite quote"}
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


class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ["title"]


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["prompt"]


class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ["text"]


class AnswerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        options = kwargs.pop("options")
        # Options must be a list of Option objects
        choices = {(o.pk, o.text) for o in options}
        super().__init__(*args, **kwargs)
        option_field = forms.ChoiceField(choices=choices, widget=forms.RadioSelect, required=True)
        self.fields["option"] = option_field


class BaseAnswerFormSet(forms.BaseFormSet):
    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs["options"] = kwargs["options"][index]
        return kwargs
