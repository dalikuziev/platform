from django.apps import AppConfig

class GroupsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.v1.groups'

    def ready(self):
        import apps.v1.groups.signals # noqa