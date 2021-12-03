from django.contrib import admin
from simulations.models import IPR, Fluid, Role
# Register your models here.

admin.site.register(IPR)
admin.site.register(Fluid)
admin.site.register(Role)