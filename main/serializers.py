from rest_framework import serializers
from simulations.models import IPR, Fluid, Well, Separator


# this class used for serialize Fluid model:
class FluidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fluid
        fields = '__all__'


# this class used for serialize IPR model
class IPRSerializer(serializers.ModelSerializer):
    class Meta:
        model = IPR
        fields = '__all__'

# this class used for serialize Well model
class WellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Well
        fields = '__all__'

# this class used for serialize Separator model
class SeparatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Well
        fields = '__all__'






