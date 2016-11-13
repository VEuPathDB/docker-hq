from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.conf import settings
from orclservices.oracleservices import OracleServices

def index(request):
  template = loader.get_template('orclservices/index.html')
  os = OracleServices()
  context = {
    'settings' : settings,
    'oracle_services' : os.data_for_display(),
  }
  return HttpResponse(template.render(context, request))

def dashboard(request):
  template = loader.get_template('orclservices/dashboard.html')
  context = {}
  return HttpResponse(template.render(context, request))

