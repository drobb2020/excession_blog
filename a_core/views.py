import logging

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from a_blog.models import Post

logger = logging.getLogger(__name__)


def index(request):
    posts = Post.objects.all()
    logger.debug("This is a debug message.")
    logger.info("This is a info message.")
    logger.warning("This is a warning message.")
    logger.error("This is a error message.")
    logger.critical("This is a critical message.")

    context = {"posts": posts}
    return render(request, "a_core/index.html", context)


class AboutPageView(TemplateView):
    template_name = "a_core/about.html"


class ContactPageView(TemplateView):
    template_name = "a_core/contact.html"


def is_staff(user):
    return user.is_staff


@user_passes_test(is_staff)
def view_log_file(request, filename):
    file_path = settings.BASE_DIR / filename
    if file_path.exists():
        with open(file_path, 'r') as file:
            response = HttpResponse(file.read(), content_type="text/plain")
            return response
    else:
        raise Http404("Log file does not exist!")
