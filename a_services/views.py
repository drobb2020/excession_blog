import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.views.generic import TemplateView

from a_profile.models import Profile

from .forms import (
    CreateTicketForm,
    ReviewApprovalForm,
    ReviewForm,
    SubscribeForm,
    TaskForm,
    TaskUpdateForm,
    UpdateTicketForm,
)
from .models import Review, Task, Ticket

User = get_user_model()


@login_required
def review(request):
    reviews = Review.objects.filter(approved=True)
    form = ReviewForm()
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.email = request.user.email
            review.save()
            messages.success(
                request, "Thank you for submitting a review of this website."
            )
            return redirect("reviews")
    context = {"form": form, "reviews": reviews}
    return render(request, "a_services/reviews.html", context)


@login_required
def review_unapproved(request):
    reviews = Review.objects.filter(approved=False)
    context = {"reviews": reviews}
    return render(request, "a_services/review_unapproved.html", context)


@login_required
def review_approve(request, pk):
    review = Review.objects.get(pk=pk)
    form = ReviewApprovalForm(instance=review)
    if request.method == "POST":
        form = ReviewApprovalForm(request.POST, instance=review)
        if form.is_valid():
            approval = form.save(commit=False)
            approval.approved = True
            approval.save()
            messages.success(request, "Review has been approved.")
            return redirect("reviews")
    context = {"form": form}
    return render(request, "a_services/review_approve.html", context)


class CookieView(TemplateView):
    template_name = "a_services/cookie.html"


class CopyrightView(TemplateView):
    template_name = "a_services/copyright.html"


class DcmaPolicyView(TemplateView):
    template_name = "a_services/dcma_policy.html"


class DisclaimerView(TemplateView):
    template_name = "a_services/disclaimer.html"


class MemberPostAgreementView(TemplateView):
    template_name = "a_services/member_post_agreement.html"


class PrivacyView(TemplateView):
    template_name = "a_services/privacy.html"


class TermsAndConditionsView(TemplateView):
    template_name = "a_services/terms_and_conditions.html"


class TermsOfUseView(TemplateView):
    template_name = "a_services/terms_of_use.html"


@login_required
def dashboard(request):
    pending_tickets = Ticket.objects.filter(
        created_by=request.user, ticket_status="Pending"
    ).count()
    active_tickets = Ticket.objects.filter(
        created_by=request.user, ticket_status="Active"
    ).count()
    completed_tickets = Ticket.objects.filter(
        created_by=request.user, ticket_status="Completed"
    ).count()
    eng_pending = Ticket.objects.filter(ticket_status="Pending").count()
    eng_active = Ticket.objects.filter(ticket_status="Active").count()
    eng_completed = Ticket.objects.filter(ticket_status="Completed").count()
    context = {
        "pending_tickets": pending_tickets,
        "active_tickets": active_tickets,
        "completed_tickets": completed_tickets,
        "eng_pending": eng_pending,
        "eng_active": eng_active,
        "eng_completed": eng_completed,
    }
    return render(request, "a_services/dashboard.html", context)


# View ticket details
@login_required
def ticket_details(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    t = User.objects.get(username=ticket.created_by)
    tickets_per_user = t.created_by.all()
    context = {"ticket": ticket, "tickets_per_user": tickets_per_user}
    return render(request, "a_services/ticket_details.html", context)


""" For Customers """


# Create a ticket
@login_required
def create_ticket(request):
    if request.method == "POST":
        form = CreateTicketForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.created_by = request.user
            var.ticket_status = "Pending"
            var.save()
            messages.info(
                request,
                "Ticket successfully submitted, an engineer will be in touch.",
            )
            return redirect("dashboard")
        else:
            messages.warning(
                request, "Something went wrong, please check your form inputs."
            )
            return redirect("create-ticket")
    else:
        form = CreateTicketForm()
        context = {"form": form}
        return render(request, "a_services/create_ticket.html", context)


# Updating a ticket
@login_required
def update_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    if not ticket.is_resolved:
        if request.method == "POST":
            form = UpdateTicketForm(request.POST, instance=ticket)
            if form.is_valid():
                form.save()
                messages.info(
                    request,
                    "Your ticket info has been updated.",
                )
                return redirect("dashboard")
            else:
                messages.warning(
                    request, "Something went wrong, please check your inputs."
                )
                return redirect("update-ticket")
        else:
            form = UpdateTicketForm(instance=ticket)
            context = {"form": form}
            return render(request, "a_services/update_ticket.html", context)
    else:
        messages.warning(request, "You cannot make changes to a closed ticket")
        return redirect("dashboard")


# View all tickets
@login_required
def all_tickets(request):
    tickets = Ticket.objects.filter(created_by=request.user).order_by("-date_created")
    context = {"tickets": tickets}
    return render(request, "a_services/all_tickets.html", context)


""" For Engineers """


# View the ticket queue
@login_required
def ticket_queue(request):
    tickets = Ticket.objects.filter(ticket_status="Pending")
    context = {"tickets": tickets}
    return render(request, "a_services/ticket_queue.html", context)


# Accept a ticket from the queue
@login_required
def accept_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    ticket.assigned_to = request.user
    ticket.ticket_status = "Active"
    ticket.date_accepted = datetime.datetime.now()
    ticket.save()
    messages.info(
        request,
        "Ticket accepted. Please contact customer to resolve issue!",
    )
    return redirect("workspace")


# Close a ticket
@login_required
def close_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    ticket.ticket_status = "Completed"
    ticket.date_resolved = datetime.datetime.now()
    ticket.is_resolved = True
    ticket.save()
    messages.info(
        request,
        "Ticket has been closed. Good work, keep it up!",
    )
    return redirect("ticket-queue")


# Assigned tickets per engineer
@login_required
def workspace(request):
    tickets = Ticket.objects.filter(assigned_to=request.user, is_resolved=False)
    context = {"tickets": tickets}
    return render(request, "a_services/workspace.html", context)


# Resolved tickets
@login_required
def all_closed_tickets(request):
    tickets = Ticket.objects.filter(assigned_to=request.user, is_resolved=True)
    context = {"tickets": tickets}
    return render(request, "a_services/all_closed_tickets.html", context)


# Newsletter Subscriptions
@login_required
def subscribe(request):
    if request.method == "POST":
        form = SubscribeForm(request.POST)
        if form.is_valid():
            subscriber = form.save()
            context = {"email": subscriber.email, "name": subscriber.name}
            email_content = render_to_string(
                "a_services/subscription_thank_you.html", context
            )
            email_subject = "Thank You for Subscribing"
            recipient_list = [subscriber.email]
            from_email = settings.EMAIL_HOST_USER

            send_mail(
                email_subject,
                " ",
                from_email,
                recipient_list,
                html_message=email_content,
                fail_silently=False,
            )
            return render(request, "a_services/thank_you.html")
    else:
        form = SubscribeForm()
        context = {"form": form}
        return render(request, "a_services/subscribe.html", context)


@login_required
def task_list(request):
    tasks = Task.objects.all()
    context = {"tasks": tasks}
    return render(request, "a_services/task-list.html", context)


@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect("tasks")
    else:
        form = TaskForm()
        context = {"form": form}
        return render(request, "a_services/task-create.html", context)


@login_required
def task_detail(request, pk):
    task = Task.objects.get(pk=pk)
    context = {"task": task}
    return render(request, "a_services/task-detail.html", context)


@login_required
def task_update(request, pk):
    task = Task.objects.get(pk=pk)
    if request.method == "POST":
        form = TaskUpdateForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("tasks")
    else:
        form = TaskUpdateForm(instance=task)
        context = {"form": form}
        return render(request, "a_services/task-update.html", context)


@login_required
def task_delete(request, pk):
    task = Task.objects.get(pk=pk)
    if request.method == "POST":
        task.delete()
        return redirect("tasks")
    context = {"task": task}
    return render(request, "a_services/task-delete.html", context)
