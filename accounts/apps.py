from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"
    verbose_name = "Пользователи"

    def ready(self):
        # Register receivers
        from . import receivers

