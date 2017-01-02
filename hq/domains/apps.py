from django.apps import AppConfig

class DomainsConfig(AppConfig):
  name = 'domains'

  def ready(self):
    from domains.schedules import add_schedules
    add_schedules()
