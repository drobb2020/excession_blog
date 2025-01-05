from django.urls import path

from . import views

urlpatterns = [
    path("", views.profile_view, name="profile"),
    path('edit/', views.profile_edit_view, name="profile-edit"),
    path('onboarding/', views.profile_edit_view, name="profile-onboarding"),
    path('settings/', views.profile_settings_view, name="profile-settings"),
    path('emailchange/', views.profile_emailchange, name="profile-emailchange"),
    path('emailverify/', views.profile_emailverify, name="profile-emailverify"),
    path('delete/', views.profile_delete_view, name="profile-delete"),
    path("surveys/", views.survey_list, name="survey-list"),
    path("surveys/<int:pk>/", views.detail, name="survey-detail"),
    path("surveys/create/", views.create, name="survey-create"),
    path("surveys/<int:pk>/delete/", views.delete, name="survey-delete"),
    path("surveys/<int:pk>/edit/", views.edit, name="survey-edit"),
    path("surveys/<int:pk>/question/", views.question_create, name="survey-question-create"),
    path(
        "surveys/<int:survey_pk>/question/<int:question_pk>/option/",
        views.option_create,
        name="survey-option-create",
    ),
    path("surveys/<int:pk>/start/", views.start, name="survey-start"),
    path("surveys/<int:survey_pk>/submit/<int:sub_pk>/", views.submit, name="survey-submit"),
    path("surveys/<int:pk>/thanks/", views.thanks, name="survey-thanks"),
]
