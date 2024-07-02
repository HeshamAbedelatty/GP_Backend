from django.apps import AppConfig


class ForgetpasswordConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'forgetPassword'

    def ready(self):
        import forgetPassword.signals