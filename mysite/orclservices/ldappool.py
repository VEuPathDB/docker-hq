import ldap
from django.conf import settings
from ldappool import ConnectionManager

class LdapPool(object):

  def __init__(self):
    print("DEBUG: LdapPool init")
    self.connection_manager = ConnectionManager(
      uri=settings.LDAP_HOST,
      bind=settings.LDAP_USERNAME,
      passwd=settings.LDAP_PASSWORD,
      timeout=10,
      use_tls=True,
    )
