from cerberus import Validator
from dataclasses import dataclass
import math
import numpy as np

######################################################################################
######################### this file implemented only for    ######################
######################### example so has no real world uses ######################
######################################################################################

@dataclass
class HagedornBrown:
    # ### Fluid Model
    # # General Fields
    bubble_point_pressure_correlation: str = None
    flow_rate_at_test_buttom_hole_pressure: float = None
    gas_composition: float = None
    gas_oil_ratio: float = None
    gas_specific_gravity: float = None
    gas_viscosity: float = None
    oil_composition: float = None
    oil_gravity: float = None
    oil_specific_gravity: float = None
    oil_viscosity: float = None
    saturate_pressure: float = None
    static_buttom_hole_pressure: float = None
    test_buttom_hole_pressure: float = None
    total_flow_rate: float = None
    water_cut: float = None
    water_salinity: float = None
    water_specific_gravity: float = None
    # Gas Impurities
    co2: float = None
    h2s: float = None
    n2: float = None
    # Correlations
    bubble_point_pressure_correlation: str = None
    oil_gravity_correlation: str = None
    gas_impurities_correlation: str = None
    gas_oil_ratio_correlation: str = None
    gas_specific_gravity_correlation: str = None
    oil_gravity_correlation: str = None
    water_cut_correlation: str = None
    water_specific_gravity_correlation: str = None
    ### Separator Model
    depth_of_separator_installation: float = None
    # Separator Related
    gas_density: float = None
    oil_api: float = None
    water_density: float = None
    water_viscosity: float = None
    # Pump Related
    gor_at_pump_inlet: float = None
    oil_bubble_point_pressure_at_inlet: float = None
    oil_density_at_pump_inlet: float = None
    oil_pressure_at_pump_inlet: float = None
    oil_temperature_at_pump_inlet: float = None
    wellhead_pressure: float = None

    def __init__(self, fields:dict = None):
        if fields is not None:
            for key in fields.keys():
                if key in fields.keys():
                    self.__setattr__(key, fields[key])

class HagedornBrownValidator(Validator):

    BUBBLE_POINT_PRESSURE_CORRELATIONS = [
        'STANDING',
        'VAZQUEZ-BEGGS',
        'GLASO',
        'ALMARHOUN',
        'FARSHAD',
        'DINDORUK-CHRISTMAN',
        'PETROSKY FARSHAD',
        'LASATER',
    ]

    SCHEMA = {
        'bubble_point_pressure': {
            'type': 'float',
            'nullable': True,
        },
        'oil_gravity': {
            'type': 'float',
            'min': 1,
            'max': 38.99,
            'nullable': True,
        },
        'bubble_point_pressure_correlation': {
            'type': 'string',
            'allowed': BUBBLE_POINT_PRESSURE_CORRELATIONS,
            'nullable': True,
        },
    }

    def validate_hagedorn_brown(self, obj):
        return self.validate(obj.__dict__)


######################## Hagedorn Brown Method, Validation example ##########################
# v = HagedornBrownValidator(HagedornBrownValidator.SCHEMA)
# h = HagedornBrown({
#     'bubble_point_pressure_correlation': 'GLASO',
#     'oil_gravity': 27.2,
#     'bubble_point_pressure': 21,
# })

# if v.validate_hagedorn_brown(h):
#     print('Validation was Successful')
#     print(v.document)
# else:
#     print('Validation was Unsuccessful')
#     print(v.errors)
#     print(v.document)
