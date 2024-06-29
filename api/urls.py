from django.urls import path

from . import views

urlpatterns = [
    path("posts/", views.getPosts),
    path("posts/<int:pk>/", views.getPost),
    path("reviews/", views.getReviews),
    path("reviews/<int:pk>/", views.getReview),
]
