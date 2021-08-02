from django.apps import AppConfig


class MateriaisConfig(AppConfig):
    name = 'webdev.materiais'

    def ready(self):
        import webdev.materiais.signals