from django.apps import AppConfig


class StationsConfig(AppConfig):
    name = 'stations'

    def ready(self):
        import stations.signals
