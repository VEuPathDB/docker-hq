from django.conf.urls import url
from . import views

app_name = 'orclservices'

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'dashboard/$', views.dashboard, name='dashboard'),
]
