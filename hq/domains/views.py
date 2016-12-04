from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.template import loader

from .models import Domain
from .models import Whois

# http://cryto.net/pythonwhois/usage.html
from pythonwhois import get_whois
import datetime
import pytz
from django.core import serializers


def index(request, order_by = None):
  template = loader.get_template('domains/index.html')
  domain_list = Domain.objects.order_by('domain_name')
  context = {
    'domain_list': domain_list,
  }
  return HttpResponse(template.render(context, request))

def whois(request, domain_name = None):
  template = loader.get_template('domains/whois.html')
  whois_records = (Whois.objects.select_related('domain').filter(domain__domain_name = domain_name).order_by('domain__domain_name')
    if domain_name
    else Whois.objects.all().order_by('domain__domain_name')
  )

  #print(Domain.objects.select_related('whois').query)
  #print(Whois.objects.select_related('domain').query)
  print(whois_records.query)
  print (whois_records)
  for rec in whois_records:
    print(rec.domain.domain_name)
  #whois_records = serializers.serialize( "python", whois_records)
  context = {
    'whois_records' : whois_records,
    'domain_name' : domain_name,
  }
  return HttpResponse(template.render(context, request))


def update_whois(request, domain_name = None):
  # for each domain name in Domains.domain, do whois lookup,
  # insert or update related whois record
  domain_list = (Domain.objects.filter(domain_name = domain_name)
    if domain_name
    else Domain.objects.all()
  )
  for domain in domain_list:
    print("Updating {0}".format(domain.domain_name))
    whois = get_whois(domain.domain_name, normalized=True)

    datadict = {}
    for k,v in whois.items():
      if not hasattr(Whois, k):
        continue
      if k == 'id': # conflicts with Model field; not needed.
        continue
      if isinstance(v, list):
        if len(v) > 1:
          datadict[k] = ','.join(v)
        else:
          if isinstance(v[0], datetime.datetime):
            datadict[k] = v[0].replace(tzinfo=pytz.utc)
          else:
            datadict[k] = v[0]
      elif isinstance(v, dict):
        datadict[k] = v
      else:
        datadict[k] = v
    datadict['internal_cache_date'] = datetime.datetime.now().replace(tzinfo=pytz.utc)
    whois_record, created = Whois.objects.update_or_create(
      domain=domain,
      defaults = datadict
    )
    domain.whois = whois_record
    domain.save()
  return_to = request.GET.get('from', reverse('domains:whois'))
  return HttpResponseRedirect(return_to)
  #return HttpResponse("whoisupdated")