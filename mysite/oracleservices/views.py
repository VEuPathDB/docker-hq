from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.conf import settings
from oracleservices.oracleservices import OracleServices
from oracleservices.ldappool import LdapPool

ldappool = LdapPool()

def index(request, host_filter = None):
  template = loader.get_template('oracleservices/index.html')
  os = OracleServices(ldappool, host_filter)
  context = {
    'settings' : settings,
    'host_filter': host_filter,
    'oracle_services': sorted(os.combined_services.items()),
  }
  return HttpResponse(template.render(context, request))

def dashboard(request):
  template = loader.get_template('oracleservices/dashboard.html')
  context = {}
  return HttpResponse(template.render(context, request))

