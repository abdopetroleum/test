from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Simulation, Membership, OdWeightId, CasingTubing, Design, Fluid


class SimulationListFields:
    def __init__(self, name, time_created, user_email, url):
        self.name = name
        self.time_created = time_created
        self.user_email = user_email
        self.url = url


class SimulationListSerialize(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    time_created = serializers.DateTimeField()
    user_email = serializers.EmailField()
    url = serializers.CharField(max_length=50)


class SimulationUpdateSerialize(serializers.ModelSerializer):
    class Meta:
        model = Simulation
        fields = ["url", "name", "description", "visibility"]

    url = serializers.CharField(
        validators=[
            UniqueValidator(
                            queryset=Simulation.objects.all(),
                            message="This url is already exists.")
                  ],
        max_length=50,
        required=False,
        error_messages={
            "max_length": "Url must be less than 50 character.",
        }
    )

    name = serializers.CharField(
        required=False,
        max_length=50,
        error_messages={
            "max_length": "Name must be less than 50 character."
        }
    )

    description = serializers.CharField(
        required=False,
        max_length=500,
        error_messages={
            "max_length": "Description must be less than 500 character."
        }
    )

    VISIBILITY_CHOICES = (
        ("1", "Private"),
        ("2", "Public"),
    )

    visibility = serializers.ChoiceField(
                        required=False,
                        choices=VISIBILITY_CHOICES, error_messages={"invalid": "sad"})


class GetSimulationSerialize(serializers.ModelSerializer):
    class Meta:
        model = Simulation
        fields = ["name", "url", "description", "visibility"]


class MembershipListFields:
    def __init__(self, user_email, role):
        self.role = role
        self.user_email = user_email



class MembershipListSerialize(serializers.Serializer):
    role = serializers.CharField(max_length=50)
    user_email = serializers.EmailField()


class OdWeightIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = OdWeightId
        fields = ["outside_diameter_OD", "inside_diameter_ID", "weight"]


class CasingTubingSerializerGet(serializers.ModelSerializer):
    class Meta:
        model = CasingTubing
        fields = ["id", "type", "bottom", "top", "inside_diameter", "outside_diameter", "roughness"]


class CasingTubingSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = CasingTubing
        fields = ["type", "bottom", "top", "inside_diameter", "outside_diameter", "roughness"]

    def validate(self, data):

        print("sssss", data["type"])

        err = []
        if data["type"] is not None:
            if str(data["type"].lower()) != "casing" and str(data["type"]).lower() != "tubing":
                err.append("Type is invalid.")
        else:
            err.append("Type is required.")

        if data["bottom"] is not None:
            pass
        else:
            err.append("Bottom is required.")

        if data["top"] is not None:
            pass
        else:
            err.append("Top is required.")

        if data["inside_diameter"] is not None:
            pass
        else:
            err.append("Inside diameter is required.")

        if data["outside_diameter"] is not None:
            pass
        else:
            err.append("Outside diameter is required.")

        if data["roughness"] is not None:
            pass
        else:
            err.append("Roughness is required.")

        outside_diameter = data["outside_diameter"]
        inside_diameter = data["inside_diameter"]

        od_id_weight = OdWeightId.objects.filter(
                            inside_diameter_ID=inside_diameter,
                            outside_diameter_OD=outside_diameter
                        )

        if len(od_id_weight) == 0:
            err.append("Inside diameter and outside diameter values are not valid.")

        if len(err) > 0:
            raise serializers.ValidationError(err)
        else:
            return data


class CasingTubingSerializerPut(serializers.ModelSerializer):
    class Meta:
        model = CasingTubing
        fields = ["id", "type", "bottom", "top", "inside_diameter", "outside_diameter", "roughness"]

    def validate(self, data):
        if str(data["type"]).lower() != "casing" and str(data["type"]).lower() != "tubing":
            raise serializers.ValidationError("Type is invalid")

        outside_diameter = data["outside_diameter"]
        inside_diameter = data["inside_diameter"]

        od_id_weight = OdWeightId.objects.filter(
                            inside_diameter_ID=inside_diameter,
                            outside_diameter_OD=outside_diameter
                        )

        if len(od_id_weight) == 0:
            raise serializers.ValidationError("Inside diameter and outside diameter values are not valid.")

        return data


class CasingTubingSerializerDelete(serializers.ModelSerializer):
    class Meta:
        model = CasingTubing
        fields = ["id"]


class DesignSerializer(serializers.ModelSerializer):

    class Meta:
        model = Design
        fields = ["fluid_rate", "pump_depth", "tubing_pressure", "casing_pressure"]

    def validate(self, data):
        err = []

        if data["fluid_rate"] is not None:
            if data["fluid_rate"] < 0 or data["fluid_rate"] > 99999:
                err.append("Fluid rate must be between 0 to 99999.")
        else:
            err.append("Fluid rate is required.")

        if data["tubing_pressure"] is not None:
            if data["tubing_pressure"] < 0 or data["tubing_pressure"] > 99999:
                err.append("Tubing pressure must be between 0 to 99999.")
        else:
            err.append("Tubing pressure is required.")

        if data["casing_pressure"] is not None:
            if data["casing_pressure"] < 0 or data["casing_pressure"] > 99999:
                err.append("Casing pressure must be between 0 to 99999.")
        else:
            err.append("Casing pressure is required.")

        if data["pump_depth"] is not None:
            pass
        else:
            err.append("Pump depth is required.")

        if len(err) > 0:
            raise serializers.ValidationError(err)
        else:
            return data


class FluidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fluid
        fields = [
            # Production data
            "oil_gravity",
            "gas_SP_GR",
            "water_cut",
            "bubble_point_pressure",
            "water_salinity",
            "water_SP_GR",
            "production_gor",
            # Gas impurities
            "co2",
            "h2s",
            "n2",
            # Seperator condition
            "tempreture",
            "pressure",
            # Correlation
            "dead_oil_viscosity_correlation",
            "saturated_oil_viscosity_correlations",
            "undersaturated_oil_viscosity",
            "gas_viscosity_correlation",
            "Oil_FVF",
            "bubble_point_pressure_correlation_option",
            "solution_GOR",
        ]

    def validate(self, data):

        err = []

        if data["oil_gravity"] is not None:
            if data["oil_gravity"] < 5 or data["oil_gravity"] > 60:
                err.append("Oil gravity must be between 5 to 60.")
        else:
            err.append("Oil gravity is required.")

        if data["gas_SP_GR"] is not None:
            if data["gas_SP_GR"] < 0.5 or data["gas_SP_GR"] > 2:
                err.append("Gas SP GR must be between 0.5 to 2.")
        else:
            err.append("Gas SP GR is required.")

        if data["water_cut"] is not None:
            if data["water_cut"] < 0 or data["water_cut"] > 100:
                err.append("Water cut must be between 0 to 100.")
        else:
            err.append("Water cut is required.")

        if data["bubble_point_pressure"] is not None:
            if data["bubble_point_pressure"] < 1 or data["bubble_point_pressure"] > 100000:
                err.append("Bubble point pressure must be between 0 to 500000.")
        else:
            err.append("Bubble point pressure is required.")

        if data["water_salinity"] is not None:
            if data["water_salinity"] < 0 or data["water_salinity"] > 500000:
                err.append("Water salinity must be between 0 to 500000.")
        else:
            err.append("Water salinity is required.")

        if data["water_SP_GR"] is not None:
            if data["water_SP_GR"] < 1 or data["water_SP_GR"] > 2.5:
                err.append("Water SP GR must be between 1 to 2.5.")
        else:
            err.append("Water SP GR is required.")

        if data["production_gor"] is not None:
            if data["production_gor"] < 1 or data["production_gor"] > 150000:
                err.append("Production gor must be between 0 to 150000.")
        else:
            err.append("Production gor is required.")

        if data["co2"] is not None:
            if data["co2"] < 0 or data["co2"] > 100:
                err.append("CO2 must be between 0 to 100.")
        else:
            err.append("CO2 is required.")

        if data["h2s"] is not None:
            if data["h2s"] < 0 or data["h2s"] > 100:
                err.append("H2S must be between 0 to 100.")
        else:
            err.append("H2S is required.")

        if data["n2"] is not None:
            if data["n2"] < 0 or data["oil_gravity"] > 100:
                err.append("N2 must be between 0 to 100.")
        else:
            err.append("N2 is required.")

        if data["tempreture"] is not None:
            if data["tempreture"] < 32 or data["tempreture"] > 600:
                err.append("Tempreture must be between 32 to 600.")
        else:
            err.append("Tempreture is required.")

        if data["pressure"] is not None:
            if data["pressure"] < 14.67 or data["pressure"] > 22000:
                err.append("Pressure must be between 14.67 to 22000.")
        else:
            err.append("Pressure is required.")

        # Correlation validation













