from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.conf import settings
from orclservices.oracleservices import OracleServices
from orclservices.ldappool import LdapPool

ldappool = LdapPool()

def index(request, host_filter = None):
  template = loader.get_template('orclservices/index.html')
  #print("REQUESTSTRING %s" % request.ldap_conn)
  os = OracleServices(ldappool, host_filter)
  context = {
    'settings' : settings,
    'oracle_services' : os.data_for_display(),
  }
  return HttpResponse(template.render(context, request))

def dashboard(request):
  template = loader.get_template('orclservices/dashboard.html')
  context = {}
  return HttpResponse(template.render(context, request))

