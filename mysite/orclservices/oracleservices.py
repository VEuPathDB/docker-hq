import re
import ldap
import math
from ldap.cidict import cidict
from django.conf import settings
from datetime import datetime

class OracleServices:

  def __init__(self, ldappool = None, host_filter = None):
    self.host_filter = host_filter
    with ldappool.connection_manager.connection() as conn:
      self.conn = conn
    self.combined_services = {}
    self.combine_service_data_from_ldap()


  def search(self, base_dn, scope = ldap.SCOPE_SUBTREE,
    attrlist = None, filterstr = None):
    try:
      return self.conn.search_s(base_dn, scope, filterstr, attrlist)
    except ldap.LDAPError as e:
      print("Error: {0}".format(e))

  def combine_service_data_from_ldap(self):
    self.processOracleLsnrctlServices()
    self.procesOracleContext()


  def procesOracleContext(self):
    dn = "cn=oraclecontext,ou=applications,dc=apidb,dc=org"
    if self.host_filter is None:
      filterstr = "(objectclass=orclNetService)"
    else:
      filterstr = "(&(objectclass=orclNetService)(orclNetDescString=*HOST={0}*))".format(self.host_filter)
    scope = ldap.SCOPE_SUBTREE
    attrlist = ["cn", "orclnetdescstring", "description"]
    result_set = self.search(dn, ldap.SCOPE_ONELEVEL, attrlist, filterstr)
    servicename_re = re.compile(".+SERVICE_NAME=([^\)]+)\).*", re.IGNORECASE)
    tnsname_re = re.compile(".+HOST=([^\)]+)\).*", re.IGNORECASE)

    if result_set is None:
      return
    for result in result_set:
      tns_entries = cidict(result[1])
      cn = tns_entries["cn"][0].decode("utf-8").strip()
      # split/join to remove all whitespace in orclNetDescString
      orclNetDescString = "".join(tns_entries["orclnetdescstring"][0].decode("utf-8").split())

      m = re.match(servicename_re, orclNetDescString)
      service_name = "NA"
      if m is not None:
        service_name = m.group(1)

      m = re.match(tnsname_re, orclNetDescString)
      tns_host = "NA"
      if m is not None:
        tns_host = m.group(1)

      svc_name_host = ("{0} {1}".format(service_name, tns_host)).lower()

      if svc_name_host not in self.combined_services:
        self.combined_services[svc_name_host] = {}
        self.combined_services[svc_name_host]["cn_list"] = []

      self.combined_services[svc_name_host]["cn_list"].append(cn)
      self.combined_services[svc_name_host]["cn_str"] = (
        ', '.join(sorted(self.combined_services[svc_name_host]["cn_list"]))
      )
      self.combined_services[svc_name_host]["tns_host"] = tns_host
      self.combined_services[svc_name_host]["service_name"] = service_name

      # attributes we want to copy over from OracleLsnrctlServices
      # for sortability.
      transfer_keys = ["instance", "verified_unix_time", "verified_date_time",
                       "created_unix_time", "created_date_time" ]
      for key in transfer_keys:
        if key not in self.combined_services[svc_name_host]:
          self.combined_services[svc_name_host][key] = ""


  def processOracleLsnrctlServices(self):
    dn = "cn=OracleLsnrctlServices,ou=applications,dc=apidb,dc=org"
    scope = ldap.SCOPE_SUBTREE
    attrlist = [
      "cn", "orclNetServer", "orclNetServiceName",
      "orclNetInstanceName", "orclVersion", "verifiedTimestamp",
      "createtimestamp"
    ]
    if self.host_filter is None:
      filterstr = "(objectclass=orclNetDescription)"
    else:
      filterstr = "(&(objectclass=orclNetDescription)(orclNetServer={0}))".format(self.host_filter)
    result_set = self.search(dn, ldap.SCOPE_ONELEVEL, attrlist, filterstr)
    if result_set is None:
      return
    for result in result_set:
      srvc_entries = cidict(result[1])
      orclNetServiceName = srvc_entries["orclnetservicename"][0].decode("utf-8").strip()
      orclNetServer = srvc_entries["orclnetserver"][0].decode("utf-8").strip()
      orclNetInstanceName = srvc_entries["orclnetinstancename"][0].decode("utf-8").strip()
      svcNameHost = ("{0} {1}".format(orclNetServiceName, orclNetServer)).lower()
      verifiedTimestamp = srvc_entries["verifiedtimestamp"][0].decode("utf-8")
      verified_date_obj = datetime.strptime(verifiedTimestamp, "%Y%m%d%H%M%SZ")
      verified_unix_time = (verified_date_obj - datetime(1970, 1, 1)).total_seconds()
      verified_date_time = self.time_since(verified_date_obj)
      createTimestamp = srvc_entries["createtimestamp"][0].decode("utf-8")
      created_date_obj = datetime.strptime(createTimestamp, "%Y%m%d%H%M%SZ")
      created_date_time = datetime.strftime(created_date_obj, "%-d %b %Y")
      created_unix_time = (created_date_obj - datetime(1970, 1, 1)).total_seconds()

      #print("{0} ago".format(verified_date_time))
      #print("{0}".format(svcNameHost))

      self.combined_services[svcNameHost] = {}
      self.combined_services[svcNameHost]["cn_list"] = []
      self.combined_services[svcNameHost]["tns_host"] = orclNetServer
      self.combined_services[svcNameHost]["service_name"] = orclNetServiceName
      self.combined_services[svcNameHost]["redmine_link"] = self.make_redmine_link(orclNetServiceName)
      self.combined_services[svcNameHost]["instance"] = orclNetInstanceName
      self.combined_services[svcNameHost]["created_unix_time"] = created_unix_time
      self.combined_services[svcNameHost]["created_date_time"] = created_date_time
      self.combined_services[svcNameHost]["verified_date_time"] = verified_date_time
      self.combined_services[svcNameHost]["verified_unix_time"] = verified_unix_time # for sorting


  def make_redmine_link(self, orclNetServiceName):
    redmine_re = re.compile("^rm([0-9]+).*", re.IGNORECASE)
    m = re.match(redmine_re, orclNetServiceName)
    if m is not None:
      redmine_link = "https://redmine.apidb.org/issues/{0}".format(m.group(1))
      return "<a href='{0}'>{1}&nbsp;&reg;<a>".format(redmine_link, orclNetServiceName)
    return None



  """
    Given a start_date as a datetime.datetime object, return a string
    describing the time elapsed since start_date. The elapsed time
    displayed is limited to at most two time units, with minutes being the
    smallest unit as the following examples illustrate,
      1 year 1 month
      3 days 5 hrs
      4 hrs 40 mins
      40 mins
  """
  def time_since(self, start_date):

    chunks = [
        [60 * 60 * 24 * 365, "year"],
        [60 * 60 * 24 * 30 , "month"],
        [60 * 60 * 24 * 7,   "week"],
        [60 * 60 * 24,       "day"],
        [60 * 60,            "hr"],
        [60,                 "min"],
    ]

    now = datetime.now()
    seconds_since = (now - start_date).total_seconds()
    for idx, chunk in enumerate(chunks):
      seconds = chunk[0]
      name = chunk[1]
      # finding the biggest chunk (if the chunk fits, break)
      count = math.floor(seconds_since/seconds)
      if (count != 0):
        break

    display_str = ("1 {0}".format(name)) if (count == 1) else ("{0} {1}s".format(count, name))

    if idx + 1 < len(chunks):
      # now getting the second time chunk
      seconds_2 = chunks[idx + 1][0]
      name_2 = chunks[idx + 1][1]
      # add second item if it"s greater than 0
      count_2 = math.floor((seconds_since - (seconds * count)) / seconds_2)
      if (count_2 != 0):
        display_str_2 = ("1 {0}".format(name_2)) if (count_2 == 1) else ("{0} {1}s".format(count_2, name_2))
        display_str = "{0} {1} ago".format(display_str, display_str_2)

    return display_str

  """
    Return dictionary ready for rendering as an html table.
  """
  def data_for_display(self):
    table_headers = []
    table_rows = []
    header_key = [
      ["service_name", "service_name"], 
      ["net service name", "cn_list"],
      ["host", "tns_host"],
      ["instance", "instance"],
      ["verified", "verified_date_time"],
      ["service registered", "created_date_time"],
    ]
    redmine_re = re.compile("^rm([0-9]+).*", re.IGNORECASE)

    for row in header_key:
      table_headers.append(row[0])

    for key, entry in sorted(self.combined_services.items()):
      row = {}
      row['fields'] = []
      row['state'] = None

      m = re.match(redmine_re, entry['instance'] )
      if m is not None:
        redmine_link = "https://redmine.apidb.org/issues/{0}".format(m.group(1))
        entry['service_name'] = "<a href='{0}'>{1}&nbsp;&reg;<a>".format(redmine_link, entry['service_name'])

      for title, srvc_key in header_key:
        if isinstance(entry[srvc_key], list):
          field = ', '.join(entry[srvc_key])
        else:
          field = entry[srvc_key]
        row['fields'].append(field)

      if entry['instance'] is None or entry['instance'] == "":
        row['offline'] = '1'
      table_rows.append(row)

    table_data = {
      "headers": table_headers,
      "rows": table_rows,
    }
    return table_data
