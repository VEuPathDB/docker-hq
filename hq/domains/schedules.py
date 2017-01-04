import django_rq
from datetime import datetime, timedelta
from domains.whois import WhoisCachier
from .models import Domain
import random

queue_name = 'default'
now = datetime.utcnow()

def update(domain):
  WhoisCachier.update_whois_model(domain)

# Update whois models via RQ cron. To avoid abusing the whois server,
# schedule at random minute after fixed hour.
def add_schedules():
  scheduler = django_rq.get_scheduler('default')

  for job in scheduler.get_jobs():
    job.delete()

  for domain in Domain.objects.all():
    h = '22'
    m = str(random.randint(1, 60) -1)
    cron_string = '{0} {1} * * *'.format(m, h)
    print("scheduling whois updates for {0}, at {1}".format(domain.domain_name, cron_string))
    scheduler.cron(
      cron_string = cron_string,
      func = update,
      args = [domain],
      description = 'update {0} whois'.format(domain.domain_name),
    )


  list_of_job_instances = scheduler.get_jobs()
  print ("JOB INSTANCES {0}".format(list_of_job_instances))


