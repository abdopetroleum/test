from .models import Fluid
import django_filters

class FluidFilter(django_filters.FilterSet):
    class Meta:
        model = Fluid
        fields = Fluid.fields()