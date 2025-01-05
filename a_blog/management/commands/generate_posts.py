from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from taggit.managers import TaggableManager

from a_blog.models import Post

user = get_user_model()

author = user.objects.first()

tags = TaggableManager()


class Command(BaseCommand):
    help = "Generate blog posts for testing purposes."

    def add_arguments(self, parser):
        parser.add_argument("number_of_posts", type=int)

    def handle(self, *args, **options):
        number = options.get("number_of_posts")
        for _ in range(number):
            Post.objects.create(
                title=get_random_string(length=20),
                subtitle="UV A single tool to replace pip, pip-tools, pipx, poetry, pyenv, twine, virtualenv.",
                slug=get_random_string(length=20),
                author=author,
                content="uv provides a drop-in replacement for common pip, pip-tools, and virtualenv commands. uv extends their interfaces with advanced features, such as dependency version overrides, platform-independent resolutions, reproducible resolutions, alternative resolution strategies, and more. Migrate to uv without changing your existing workflows — and experience a 10-100x speedup — with the uv pip interface.",
                status="Published",
                tags="testing",
            )
        print(
            f"{number} blog posts were generated for testing purposes!",
            Post.objects.all(),
            sep="\n",
        )
