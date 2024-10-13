from django.apps import AppConfig


class CmpConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cmp"

    def ready(self):
        import cmp.db_signals
