from django.conf.urls import url
from . import views

app_name = 'domains'

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^whois/$', views.whois, name='whois'),
  url(r'^whois/(?P<domain_name>[\w\.]+)/$', views.whois, name='whois'),
  url(r'^update_whois/$', views.update_whois, name='update_whois'),
  url(r'^update_whois/(?P<domain_name>[\w\.]+)/', views.update_whois, name='update_whois'),
]