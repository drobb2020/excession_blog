from django.urls import path

from . import views

urlpatterns = [
    path('', views.review, name="reviews"),
    path('cookies/', views.CookieView.as_view(), name="cookies"),
    path("copyright/", views.CopyrightView.as_view(), name="copyright"),
    path("dcma/", views.DcmaPolicyView.as_view(), name="dcma"),
    path("disclaimer/", views.DisclaimerView.as_view(), name="disclaimer"),
    path("member_post_agreement/", views.MemberPostAgreementView.as_view(), name="member_post_agreement"),
    path("privacy/", views.PrivacyView.as_view(), name="privacy"),
    path("terms_and_conditions/", views.TermsAndConditionsView.as_view(), name="terms_and_conditions"),
    path("terms_of_use/", views.TermsOfUseView.as_view(), name="terms_of_use"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path("ticket-details/<int:pk>/", views.ticket_details, name="ticket-details"),
    path("create-ticket/", views.create_ticket, name="create-ticket"),
    path("update-ticket/<int:pk>/", views.update_ticket, name="update-ticket"),
    path("all-tickets/", views.all_tickets, name="all-tickets"),
    path("ticket-queue/", views.ticket_queue, name="ticket-queue"),
    path("accept-ticket/<int:pk>/", views.accept_ticket, name="accept-ticket"),
    path("close-ticket/<int:pk>/", views.close_ticket, name="close-ticket"),
    path("workspace/", views.workspace, name="workspace"),
    path("all-closed-tickets/", views.all_closed_tickets, name="all-closed-tickets"),
]
