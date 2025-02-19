from django.apps import AppConfig


class PharmacyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pharmacy_app'

    def ready(self):
        import pharmacy_app.signals