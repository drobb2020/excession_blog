from django.urls import path

from . import views

urlpatterns = [
    path("", views.post_list, name="posts"),
    path('tag/<slug:tag>/', views.TagListView.as_view(), name='post_by_tag'),
    path("create/", views.post_create, name="post-create"),
    path("status/", views.post_status, name="post-status"),
    path("search/", views.SearchResultsListView.as_view(), name="search-results"),
    path("<slug:post>/", views.post_detail, name="post-detail"),
    path("<slug:post>/update/", views.post_update, name="post-update"),
    path("<slug:post>/delete/", views.post_delete, name="post-delete"),
    path("<slug:post>/status/", views.update_status, name="update-status"),
    path('generate_pdf/<slug:post>/', views.post_render_pdf_view, name='generate-pdf'),
]
