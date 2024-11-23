from django.apps import AppConfig


class UserEditConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_edit'

    def ready(self):
        import user_edit.signals  # Import the signals

