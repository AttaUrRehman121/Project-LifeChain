from django.apps import AppConfig


class RecipientConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recipient'
    
    def ready(self):
        import recipient.signals
