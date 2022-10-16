from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'share_thoughts'
    def ready(self):
        import share_thoughts.signals
