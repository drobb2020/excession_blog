from django.shortcuts import render
from django.views.generic import TemplateView

from a_blog.models import Post


def index(request):
    posts = Post.objects.all()
    context = {"posts": posts}
    return render(request, "a_core/index.html", context)


class AboutPageView(TemplateView):
    template_name = "a_core/about.html"


class ContactPageView(TemplateView):
    template_name = "a_core/contact.html"
