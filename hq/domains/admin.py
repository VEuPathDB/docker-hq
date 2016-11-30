from django.contrib import admin

from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin

from .models import Domain
from .models import Registrar
from .models import Registrant

# Create a related record as needed.
class RelationWidget(ForeignKeyWidget):
  def clean(self, value, row=None, *args, **kwargs):
    return self.model.objects.get_or_create(name = value)[0]

class DomainResource(resources.ModelResource):
  registrar = fields.Field(
    column_name='registrar',
    attribute='registrar',
    widget=RelationWidget(Registrar, 'name')
  )
  registrant = fields.Field(
    column_name='registrant',
    attribute='registrant',
    widget=RelationWidget(Registrant, 'name')
  )

  class Meta:
    model = Domain
    skip_unchanged = True
    report_skipped = True
    fields = ('id', 'domain_name', 'registrar', 'registrant', 'notes')
    export_order = ('id', 'domain_name', 'registrar', 'registrant', 'notes')

class DomainAdmin(ImportExportModelAdmin):
    resource_class = DomainResource

admin.site.register(Domain, DomainAdmin)
admin.site.register(Registrar)
admin.site.register(Registrant)
