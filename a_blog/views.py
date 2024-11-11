from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import get_template
from django.urls import reverse
from django.views.generic import ListView
from taggit.models import Tag
from xhtml2pdf import pisa

from .forms import CommentForm, PostCreateForm, PostStatusForm, PostUpdateForm
from .models import Comment, Post


def post_list(request):
    posts = Post.objects.filter(Q(status="Published"))
    tags = Tag.objects.all()
    context = {"posts": posts, "tags": tags}
    return render(request, "a_blog/post_list.html", context)


class TagListView(ListView):
    model = Post
    paginate_by = 10
    context_object_name = "posts"

    def get_queryset(self):
        x = Post.objects.filter(tags__name__in=[self.kwargs["tag"]])
        return x

    def get_template_names(self):
        return "a_blog/tags.html"

    def get_context_data(self, **kwargs):
        context = super(TagListView, self).get_context_data(**kwargs)
        context["tag"] = self.kwargs["tag"]
        return context


def post_detail(request, post):
    post = get_object_or_404(Post, slug=post)
    comments = Comment.objects.filter(post=post)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
    else:
        form = CommentForm()
    context = {"post": post, "comments": comments, "form": form}
    return render(request, "a_blog/post_detail.html", context)


@login_required
def post_create(request):
    form = PostCreateForm(request.POST or None, request.FILES or None)
    author = request.user
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            messages.success(
                request,
                "Your post has been successfully submitted. It will be reviewed and approved shortly.",
            )
            return redirect(reverse("posts"))

    context = {"form": form}
    return render(request, "a_blog/post_create.html", context)


@login_required
def post_update(request, post):
    post = get_object_or_404(Post, slug=post)
    form = PostUpdateForm(request.POST or None, request.FILES or None, instance=post)
    author = request.user
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            messages.success(request, "Your post has been successfully updated.")
            return redirect(reverse("posts"))
    context = {"form": form}
    return render(request, "a_blog/post_update.html", context)


@login_required
def post_delete(request, post):
    post = get_object_or_404(Post, slug=post)
    post.delete()
    messages.success(request, "Your post has been deleted.")
    return redirect(reverse("posts"))


@login_required
def post_status(request):
    posts = Post.objects.filter(status="draft")
    context = {"posts": posts}
    return render(request, "a_blog/post_status.html", context)


@login_required
def update_status(request, post):
    post = get_object_or_404(Post, slug=post)
    form = PostStatusForm(request.POST or None, instance=post)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "The post has been approved.")
            return redirect(reverse("posts"))
    context = {"form": form}
    return render(request, "a_blog/update_status.html", context)


class SearchResultsListView(ListView):
    model = Post
    context_object_name = "post_list"
    template_name = "a_blog/post_search_results.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        return Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )


def post_render_pdf_view(request, post):
    post = get_object_or_404(Post, slug=post)
    template_path = "a_blog/post_pdf_template.html"
    context = {"post": post}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="excession-post.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse("We had some errors <pre>" + html + "</pre>")
    return response
