from django.db import models

class Registrar(models.Model):
  name = models.CharField(max_length=50, null=False, unique=True)
  def __str__(self):
    return self.name

class Registrant(models.Model):
  name = models.CharField(max_length=50, null=False, unique=True)
  def __str__(self):
    return self.name

class Domain(models.Model):
  domain_name = models.CharField(max_length=50, null=False, unique=True)
  registrar = models.ForeignKey(Registrar, on_delete=models.CASCADE)
  registrant = models.ForeignKey(Registrant, on_delete=models.CASCADE)
  notes = models.CharField(max_length=250, blank=True, null=True)
  def __str__(self):
    return self.domain_name
