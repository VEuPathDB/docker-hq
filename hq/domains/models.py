from django.db import models

class Registrar(models.Model):
  name = models.CharField(max_length=50, null=False, unique=True)
  def __str__(self):
    return self.name

class Registrant(models.Model):
  name = models.CharField(max_length=50, null=False, unique=True)
  def __str__(self):
    return self.name

class Whois(models.Model):
  contacts = models.CharField(max_length=50, blank=True, null=True)
  registrar = models.CharField(max_length=50, blank=True, null=True)
  nameservers = models.CharField(max_length=50, blank=True, null=True)
  status = models.CharField(max_length=50, blank=True, null=True)
  creation_date =  models.DateTimeField(blank=True, null=True)
  updated_date = models.DateTimeField(blank=True, null=True)
  expiration_date = models.DateTimeField(blank=True, null=True)
  internal_cache_date = models.DateTimeField(auto_now_add=True)
  def __str__(self):
    return str(self.id)

class Domain(models.Model):
  domain_name = models.CharField(max_length=50, null=False, unique=True)
  whois = models.OneToOneField(Whois, on_delete=models.CASCADE, blank=True, null=True) #models.ForeignKey(Whois, on_delete=models.CASCADE, blank=True, null=True)
  registrar = models.ForeignKey(Registrar, on_delete=models.CASCADE)
  registrant = models.ForeignKey(Registrant, on_delete=models.CASCADE)
  notes = models.CharField(max_length=250, blank=True, null=True)
  def __str__(self):
    return self.domain_name
