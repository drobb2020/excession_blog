from django import forms

from .models import Review, Subscriber, Task, Ticket


class ReviewForm(forms.ModelForm):

    class Meta:
        comment = forms.CharField(
            widget=forms.Textarea(attrs={"placeholder": "Add your review here..."})
        )

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
        fields = ["name", "email"]


class TaskForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Add a new Task"}))
    description = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Add a description"}))
    due_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "due_date",
            "is_completed",
        ]


class TaskUpdateForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Add a new Task"}))
    description = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Add a description"}))
    completed_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "due_date",
            "is_completed",
            "completed_date",
        ]
