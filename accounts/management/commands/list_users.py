from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()

users = User.objects.all()


class Command(BaseCommand):
    help = "List all the current accounts that have access to this blog site."

    def handle(self, *args, **kwargs):
        for user in users:
            print(f'user is {user.get_full_name()}, their username is {user.get_username()}')
