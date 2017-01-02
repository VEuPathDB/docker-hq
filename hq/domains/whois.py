# http://cryto.net/pythonwhois/usage.html
from datetime import datetime
from pytz import utc
from .models import Domain
from .models import Whois
from django.core import serializers
from pythonwhois import get_whois
from pythonwhois.shared import WhoisException

class WhoisCachier:

  def update_whois_model(domain_model):
    try:
      whois = get_whois(domain_model.domain_name, normalized=True)
    except Exception as err:
      print("upate_whois() failed: {0}".format(err))
      return
    datadict = {}
    for k,v in whois.items():
      if not hasattr(Whois, k):
        continue # skip whois fields not in our model
      if k == 'id':
        continue # conflicts with Model field; also is irrelevant data
      if isinstance(v, list):
        if len(v) > 1:
          datadict[k] = ','.join(v)
        else:
          if isinstance(v[0], datetime):
            datadict[k] = v[0].replace(tzinfo=utc)
          else:
            datadict[k] = v[0]
      elif isinstance(v, dict):
        datadict[k] = v
      else:
        datadict[k] = v
    datadict['internal_cache_date'] = datetime.now().replace(tzinfo=utc)
    whois_record, created = Whois.objects.update_or_create(
      domain=domain_model,
      defaults = datadict
    )
    domain_model.whois = whois_record
    domain_model.save()
