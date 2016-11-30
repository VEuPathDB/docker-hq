from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Domain

def index(request, host_filter = None):
  template = loader.get_template('domains/index.html')
  domain_list = Domain.objects.order_by('domain_name')
  context = {
    'domain_list': domain_list
  }
  return HttpResponse(template.render(context, request))
