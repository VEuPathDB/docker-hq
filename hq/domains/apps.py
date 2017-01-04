from django.apps import AppConfig

class DomainsConfig(AppConfig):
  name = 'domains'

  def ready(self):
    #
    # I think the scheduling setup should not go in ready() because it
    # performs database queries - which fail if the database is not yet
    # ready (e.g. has not been migrated). See also the Warning to this
    # effect at
    # https://docs.djangoproject.com/en/1.10/ref/applications/#django.apps.AppConfig.ready
    #
    from redis.exceptions import ConnectionError
    from django.db.utils import OperationalError
    from domains.schedules import add_schedules
    try:
      add_schedules()
    except ConnectionError as ce:
      print("Skipping {0} scheduling: {1}".format(self.name, repr(ce)))
      print('Check that Redis is reachable.')
      pass
    except OperationalError as e:
      print("Skipping {0} scheduling: {1}".format(self.name, repr(e)))
      print('Check that Database is reachable and migrated.')
      pass
