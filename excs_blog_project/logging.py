from pathlib import Path

# from environs import Env

BASE_DIR = Path(__file__).resolve().parent.parent

# env = Env()
# Env.read_env()


DEFAULT_TIME_FORMAT = "%d/%b/%Y %H:%M:%S"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },
    "formatters": {
        "simple": {
            "format": "{levelname} {asctime:s} {name} {message}",
            "style": "{",
        },
        "verbose": {
            "format": "{levelname} {asctime:s} {name} {module}.py (line {lineno:d}) {funcName}. {message}",
            "style": "{",
        },
        "console": {
            "format": "[{asctime:s}] {message}",
            "style": "{",
            "datefmt": DEFAULT_TIME_FORMAT,
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
        "file-root": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "formatter": "verbose",
            "filename": BASE_DIR / "logs/root-logger.log",
        },
        "file-django": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "formatter": "verbose",
            "filename": BASE_DIR / "logs/django.log",
        },
        "file-django-server": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "formatter": "verbose",
            "filename": BASE_DIR / "logs/django-server.log",
        },
        "file-django-template": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "formatter": "verbose",
            "filename": BASE_DIR / "logs/django-template.log",
        },
        "file-django-db": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "formatter": "verbose",
            "filename": BASE_DIR / "logs/django-database.log",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
            "include_html": True,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "": {
            "level": "INFO",
            "handlers": ["console", "file-root", "mail_admins"],
        },
        "django": {
            "handlers": ["console", "file-django", "mail_admins"],
            "level": "INFO",
            "propagate": False,
        },
        "django.server": {
            "handlers": ["file-django-server"],
            "level": "INFO",
            "propagate": True,
        },
        "django.template": {
            "handlers": ["file-django-template"],
            "propagate": True,
            "level": "INFO",
        },
        "django.db.backends": {
            "level": "INFO",
            "handlers": ["file-django-db"],
            "propagate": False,
        },
    },
}
