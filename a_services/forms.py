from django import forms

from .models import Review, Ticket, Subscriber


class ReviewForm(forms.ModelForm):

    class Meta:
        comment = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Add your review here..."}))

        model = Review
        fields = [
            "review_title",
            "comment",
        ]


class CreateTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description"]


class UpdateTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            "title",
            "description",
            "is_resolved",
        ]


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['name', 'email']
