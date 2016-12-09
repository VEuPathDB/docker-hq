# http://cryto.net/pythonwhois/usage.html
from datetime import datetime
from pytz import utc
from .models import Domain
from .models import Whois
from django.core import serializers
from pythonwhois import get_whois

class WhoisCachier:

  def update_whois(domain_list):
    for domain in domain_list:
      whois = get_whois(domain.domain_name, normalized=True)
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
      datadict['internal_cache_date'] = datetime.now().replace(tzinfo=pytz.utc)
      whois_record, created = Whois.objects.update_or_create(
        domain=domain,
        defaults = datadict
      )
      domain.whois = whois_record
      domain.save()