from django.contrib import admin

from .models import Domain
from .models import Registrar
from .models import Registrant

admin.site.register(Domain)
admin.site.register(Registrar)
admin.site.register(Registrant)
