from django.contrib import admin
from .models import Option, Design, CasingTubing, OdWeightId, ExcelTestModel, Simulation, Well, Gearbox, Membership, Separator, Reservoir, Rod, SeparatorSize

admin.site.register(ExcelTestModel)
admin.site.register(Simulation)
admin.site.register(Gearbox)
admin.site.register(Membership)
admin.site.register(Separator)
admin.site.register(Reservoir)
admin.site.register(Rod)
admin.site.register(SeparatorSize)
admin.site.register(Well)
admin.site.register(OdWeightId)
admin.site.register(CasingTubing)
admin.site.register(Design)
admin.site.register(Option)
