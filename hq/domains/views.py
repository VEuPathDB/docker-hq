from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.template import loader

from .models import Domain
from .models import Whois

from domains.whois import WhoisCachier

def index(request, order_by = None):
  template = loader.get_template('domains/index.html')
  domain_list = Domain.objects.order_by('whois__expiration_date')
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
  WhoisCachier.update_whois(domain_list)
  return_to = request.GET.get('from', reverse('domains:whois'))
  return HttpResponseRedirect(return_to)
  #return HttpResponse("whoisupdated")