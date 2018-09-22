from django.apps import AppConfig


class OrderbotConfig(AppConfig):
    name = 'orderbot'

    def ready(self):
        import orderbot.signals