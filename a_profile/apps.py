from django.apps import AppConfig


class AProfileConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "a_profile"

    def ready(self):
        import a_profile.signals
