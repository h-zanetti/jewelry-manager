from django.apps import AppConfig


class FinanceiroConfig(AppConfig):
    name = 'webdev.financeiro'

    def ready(self):
        import webdev.financeiro.signals