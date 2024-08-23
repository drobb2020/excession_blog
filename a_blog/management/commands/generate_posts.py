from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

from a_blog.models import Post

user = get_user_model()

author = user.objects.first()


class Command(BaseCommand):
    help = "Generate blog posts for testing purposes."

    def add_arguments(self, parser):
        parser.add_argument("number_of_posts", type=int)

    def handle(self, *args, **options):
        number = options.get("number_of_posts")
        for _ in range(number):
            Post.objects.create(
                title=get_random_string(length=20),
                subtitle="If we gradle the npm, we can get to the AI Twitter through the behavior-driven SRE queue!",
                slug=get_random_string(length=20),
                author=author,
                content="Transpile build tool Edge websockets animation one-size-fits-all approach. AI compression bitwise operator FP graph bootcamp controller. DOM ELF package manager freelancer clean code promise brownfield chmod view-model DevTools. Tl;dr state Dijkstra domain specific language scale mutation observer casting Byzantine fault tolerance architecture lazy eval.",
                status="published",
                tags="testing",
            )
        print(
            f"{number} blog posts were generated for testing purposes!",
            Post.objects.all(),
            sep="\n",
        )
