from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'main'

    # Imports signals before every thing in app
    def ready(self):
        import main.signals
