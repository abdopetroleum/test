from django import forms
from django.core.exceptions import ValidationError

from main.models import Option
from .widgets import NumberInputWithUnit, NumberInput, Dropdown
from .services import ConvertUnitService


convert = ConvertUnitService()


class FluidPanelForm(forms.Form):

    # General Fields
    bubble_point_pressure = forms.FloatField(
        # min_value=1,
        # max_value=39,
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                # 'label': 'Bubble Point Pressure'
                'units': convert.target_units('bubble_point_pressure'),
                'target_unit': convert.target_unit('bubble_point_pressure'),
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'placeholder': 'bubble point pressure',
                'tooltip': 'please enter bubble point pressure value',
                'required': 'required',
            }
        ),
    )

    flow_rate_at_test_buttom_hole_pressure = forms.FloatField(
        # min_value=1,
        # max_value=39,
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                'units': convert.target_units('flow_rate_at_test_buttom_hole_pressure'),
                'target_unit': convert.target_unit('flow_rate_at_test_buttom_hole_pressure'),
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'required': 'required',
            }
        ),
    )

    gas_composition = forms.FloatField(
        # min_value=1,
        # max_value=39,
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInput(
            attrs={
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'required': 'required',
            }
        ),
    )

    gas_oil_ratio = forms.FloatField(
        # min_value=1,
        # max_value=39,
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                'units': convert.target_units('gas_oil_ratio'),
                'target_unit': convert.target_unit('gas_oil_ratio'),
                # 'min': 1,
                # 'max': 39,
                'step': 0.01,
                'required': 'required',
            }
        ),
    )

    gas_specific_gravity = forms.FloatField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInput(
            attrs={
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'required': 'required',
            }
        ),
    )
    
    gas_viscosity = forms.FloatField(
        # min_value=1,
        # max_value=39,
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                'units': [ 'cp' ],
                'target_unit': 'cp',
                'needs_conversion': False,
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'required': 'required',
            }
        ),
    )

    oil_composition = forms.FloatField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInput(
            attrs={
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'required': 'required',
            }
        ),
    )

    oil_gravity = forms.FloatField(
        min_value=1,
        max_value=39,
        error_messages={
            "min_value": "Value must be greater than 1",
            "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                'units': [ '°API' ],
                'target_unit': '°API',
                'needs_conversion': False,
                'min': 1,
                'max': 39,
                'step': 0.1,
                'required': 'required',
            }
        ),
    )
    
    oil_specific_gravity = forms.FloatField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInput(
            attrs={
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'required': 'required',
            }
        ),
    )
    
    oil_viscosity = forms.FloatField(
        # min_value=1,
        # max_value=39,
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                'units': [ 'cp' ],
                'target_unit': 'cp',
                'needs_conversion': False,
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'required': 'required',
            }
        ),
    )

    saturate_pressure = forms.FloatField(
        # min_value=1,
        # max_value=39,
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                'units': convert.target_units('saturate_pressure'),
                'target_unit': convert.target_unit('saturate_pressure'),
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'required': 'required',
            }
        ),
    )

    static_buttom_hole_pressure = forms.FloatField(
        # min_value=1,
        # max_value=39,
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                'units': convert.target_units('static_buttom_hole_pressure'),
                'target_unit': convert.target_unit('static_buttom_hole_pressure'),
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'required': 'required',
            }
        ),
    )
    
    test_buttom_hole_pressure = forms.FloatField(
        # min_value=1,
        # max_value=39,
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                'units': convert.target_units('test_buttom_hole_pressure'),
                'target_unit': convert.target_unit('test_buttom_hole_pressure'),
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'required': 'required',
            }
        ),
    )
    
    total_flow_rate = forms.FloatField(
        # min_value=1,
        # max_value=39,
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                'units': convert.target_units('total_flow_rate'),
                'target_unit': convert.target_unit('total_flow_rate'),
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'required': 'required',
            }
        ),
    )
    
    water_cut = forms.FloatField(
        min_value=0,
        max_value=100,
        error_messages={
            "min_value": "Value must be equal or greater than 0",
            "max_value": "Value must be equal or less than 100",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                'units': [ '%' ],
                'target_unit': '%',
                'needs_conversion': False,
                'min': 0,
                'max': 100,
                'step': 0.1,
                'required': 'required',
            }
        ),
    )
    
    water_salinity = forms.FloatField(
        # min_value=1,
        # max_value=39,
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                'units': [ 'ppm' ],
                'target_unit': 'ppm',
                'needs_conversion': False,
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'required': 'required',
            }
        ),
    )
    
    water_specific_gravity = forms.FloatField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInput(
            attrs={
                # 'min': 1,
                # 'max': 39,
                'step': 0.001,
                'required': 'required',
            }
        ),
    )
    
    # Gas Impurities
    co2 = forms.FloatField(
        min_value=0,
        max_value=100,
        error_messages={
            "min_value": "Value must be equal or greater than 0",
            "max_value": "Value must be equal or less than 100",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                'units': [ '%' ],
                'target_unit': '%',
                'needs_conversion': False,
                'min': 0,
                'max': 100,
                'step': 0.001,
                'required': 'required',
            }
        ),
    )

    h2s = forms.FloatField(
        min_value=0,
        max_value=100,
        error_messages={
            "min_value": "Value must be equal or greater than 0",
            "max_value": "Value must be equal or less than 100",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                'units': [ '%' ],
                'target_unit': '%',
                'needs_conversion': False,
                'min': 0,
                'max': 100,
                'step': 0.001,
                'required': 'required',
            }
        ),
    )

    n2 = forms.FloatField(
        min_value=0,
        max_value=100,
        error_messages={
            "min_value": "Value must be equal or greater than 0",
            "max_value": "Value must be equal or less than 100",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                'units': [ '%' ],
                'target_unit': '%',
                'needs_conversion': False,
                'min': 0,
                'max': 100,
                'step': 0.001,
                'required': 'required',
            }
        ),
    )

    # Correlations
    bubble_point_pressure_correlation_option = forms.CharField(
        error_messages={
            "required": "Please fill out this field",
        },
        widget=Dropdown(
            attrs={
                'required': 'required',
            },
            choices=(
                (option.value, option.display_name) for option in
                            Option.objects.filter(field_name='bubble_point_pressure_correlation_option')
            )
        ),
    )

    oil_gravity_correlation_option = forms.CharField(
        error_messages={
            "required": "Please fill out this field",
        },
        widget=Dropdown(
            attrs={
                'required': 'required',
            },
            choices=(
                (option.value, option.display_name) for option in
                            Option.objects.filter(field_name='oil_gravity_correlation_option')
            )
        ),
    )

    gas_impurities_correlation_option = forms.CharField(
        error_messages={
            "required": "Please fill out this field",
        },
        widget=Dropdown(
            attrs={
                'required': 'required',
            },
            choices=(
                (option.value, option.display_name) for option in
                            Option.objects.filter(field_name='gas_impurities_correlation_option')
            )
        ),
    )

    gas_oil_ratio_correlation_option = forms.CharField(
        error_messages={
            "required": "Please fill out this field",
        },
        widget=Dropdown(
            attrs={
                'required': 'required',
            },
            choices=(
                (option.value, option.display_name) for option in
                            Option.objects.filter(field_name='gas_oil_ratio_correlation_option')
            )
        ),
    )

    gas_specific_gravity_correlation_option = forms.CharField(
        error_messages={
            "required": "Please fill out this field",
        },
        widget=Dropdown(
            attrs={
                'required': 'required',
            },
            choices=(
                (option.value, option.display_name) for option in
                            Option.objects.filter(field_name='gas_specific_gravity_correlation_option')
            )
        ),
    )

    # oil_gravity_correlation_option = forms.CharField(
    #     error_messages={
    #         "required": "Please fill out this field",
    #     },
    #     widget=Dropdown(
    #         attrs={
    #             'required': 'required',
    #         },
    #         choices=(
    #             (option.value, option.display_name) for option in
    #                         Option.objects.filter(field_name='oil_gravity_correlation_option')
    #         )
    #     ),
    # )

    water_cut_correlation_option = forms.CharField(
        error_messages={
            "required": "Please fill out this field",
        },
        widget=Dropdown(
            attrs={
                'required': 'required',
            },
            choices=(
                (option.value, option.display_name) for option in
                            Option.objects.filter(field_name='water_cut_correlation_option')
            )
        ),
    )

    water_specific_gravity_correlation_option = forms.CharField(
        error_messages={
            "required": "Please fill out this field",
        },
        widget=Dropdown(
            attrs={
                'required': 'required',
            },
            choices=(
                (option.value, option.display_name) for option in
                            Option.objects.filter(field_name='water_specific_gravity_correlation_option')
            )
        ),
    )
    
    ### Separator Model
    depth_of_separator_installation = forms.FloatField(
        # min_value=1,
        # max_value=39,
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                # 'label': 'Bubble Point Pressure'
                'units': convert.target_units('depth_of_separator_installation'),
                'target_unit': convert.target_unit('depth_of_separator_installation'),
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'required': 'required',
            }
        ),
    )
    # Separator Related
    gas_density = forms.FloatField(
        # min_value=0,
        # max_value=100,
        error_messages={
            # "min_value": "Value must be equal or greater than 0",
            # "max_value": "Value must be equal or less than 100",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                'units': convert.target_units('gas_density'),
                'target_unit': convert.target_unit('gas_density'),
                # 'min': 0,
                # 'max': 100,
                'step': 0.1,
                'required': 'required',
            }
        ),
    )

    oil_api = forms.FloatField(
        # min_value=0,
        # max_value=100,
        error_messages={
            # "min_value": "Value must be equal or greater than 0",
            # "max_value": "Value must be equal or less than 100",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                'units': [ 'degree' ],
                'target_unit': 'degree',
                'needs_conversion': False,
                # 'min': 0,
                # 'max': 100,
                'step': 0.1,
                'required': 'required',
            }
        ),
    )

    water_density = forms.FloatField(
        # min_value=0,
        # max_value=100,
        error_messages={
            # "min_value": "Value must be equal or greater than 0",
            # "max_value": "Value must be equal or less than 100",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                'units': convert.target_units('water_density'),
                'target_unit': convert.target_unit('water_density'),
                # 'min': 0,
                # 'max': 100,
                'step': 0.1,
                'required': 'required',
            }
        ),
    )

    water_viscosity = forms.FloatField(
        # min_value=0,
        # max_value=100,
        error_messages={
            # "min_value": "Value must be equal or greater than 0",
            # "max_value": "Value must be equal or less than 100",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                'units': [ 'cP' ],
                'target_unit': 'cP',
                'needs_conversion': False,
                # 'min': 0,
                # 'max': 100,
                'step': 0.1,
                'required': 'required',
            }
        ),
    )

    # Pump Related
    gor_at_pump_inlet = forms.FloatField(
        # min_value=0,
        # max_value=100,
        error_messages={
            # "min_value": "Value must be equal or greater than 0",
            # "max_value": "Value must be equal or less than 100",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                'units': convert.target_units('gor_at_pump_inlet'),
                'target_unit': convert.target_unit('gor_at_pump_inlet'),
                # 'min': 0,
                # 'max': 100,
                'step': 0.1,
                'required': 'required',
            }
        ),
    )

    oil_bubble_point_pressure_at_inlet = forms.FloatField(
        # min_value=0,
        # max_value=100,
        error_messages={
            # "min_value": "Value must be equal or greater than 0",
            # "max_value": "Value must be equal or less than 100",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                'units': convert.target_units('oil_bubble_point_pressure_at_inlet'),
                'target_unit': convert.target_unit('oil_bubble_point_pressure_at_inlet'),
                # 'min': 0,
                # 'max': 100,
                'step': 0.1,
                'required': 'required',
            }
        ),
    )

    oil_density_at_pump_inlet = forms.FloatField(
        # min_value=0,
        # max_value=100,
        error_messages={
            # "min_value": "Value must be equal or greater than 0",
            # "max_value": "Value must be equal or less than 100",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                'units': [ 'lbm/ft^3' ],
                'target_unit': 'lbm/ft^3',
                'needs_conversion': False,
                # 'min': 0,
                # 'max': 100,
                'step': 0.1,
                'required': 'required',
            }
        ),
    )

    oil_pressure_at_pump_inlet = forms.FloatField(
        # min_value=0,
        # max_value=100,
        error_messages={
            # "min_value": "Value must be equal or greater than 0",
            # "max_value": "Value must be equal or less than 100",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                'units': convert.target_units('oil_pressure_at_pump_inlet'),
                'target_unit': convert.target_unit('oil_pressure_at_pump_inlet'),
                # 'min': 0,
                # 'max': 100,
                'step': 0.1,
                'required': 'required',
            }
        ),
    )

    oil_temperature_at_pump_inlet = forms.FloatField(
        # min_value=0,
        # max_value=100,
        error_messages={
            # "min_value": "Value must be equal or greater than 0",
            # "max_value": "Value must be equal or less than 100",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                'units': convert.target_units('oil_temperature_at_pump_inlet'),
                'target_unit': convert.target_unit('oil_temperature_at_pump_inlet'),
                # 'min': 0,
                # 'max': 100,
                'step': 0.1,
                'required': 'required',
            }
        ),
    )

    wellhead_pressure = forms.FloatField(
        # min_value=0,
        # max_value=100,
        error_messages={
            # "min_value": "Value must be equal or greater than 0",
            # "max_value": "Value must be equal or less than 100",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                'units': convert.target_units('wellhead_pressure'),
                'target_unit': convert.target_unit('wellhead_pressure'),
                # 'min': 0,
                # 'max': 100,
                'step': 0.1,
                'required': 'required',
            }
        ),
    )

    # class Meta:
    #     fields = [
    #         ### Fluid Model
    #         # General Fields
    #         'bubble_point_pressure',
    #         'flow_rate_at_test_buttom_hole_pressure',
    #         'gas_composition',
    #         'gas_oil_ratio',
    #         'gas_specific_gravity',
    #         'gas_viscosity',
    #         'oil_composition',
    #         'oil_gravity',
    #         'oil_specific_gravity',
    #         'oil_viscosity',
    #         'saturate_pressure',
    #         'static_buttom_hole_pressure',
    #         'test_buttom_hole_pressure',
    #         'total_flow_rate',
    #         'water_cut',
    #         'water_salinity',
    #         'water_specific_gravity',
    #         # Gas Impurities
    #         'co2',
    #         'h2s',
    #         'n2',
    #         # Correlations
    #         'bubble_point_pressure_correlation_option',
    #         'oil_gravity_correlation_option',
    #         'gas_impurities_correlation_option',
    #         'gas_oil_ratio_correlation_option',
    #         'gas_specific_gravity_correlation_option',
    #         'water_cut_correlation_option',
    #         'water_specific_gravity_correlation_option',
    #         ### Separator Model
    #         'depth_of_separator_installation',
    #         # Separator Related
    #         'gas_density',
    #         'oil_api',
    #         'water_density',
    #         'water_viscosity',
    #         # Pump Related
    #         "gor_at_pump_inlet",
    #         "oil_bubble_point_pressure_at_inlet",
    #         "oil_density_at_pump_inlet",
    #         "oil_pressure_at_pump_inlet",
    #         "oil_temperature_at_pump_inlet",
    #         "wellhead_pressure",
    #     ]

    field_order = [
        ### Fluid Model
        # General Fields
        'bubble_point_pressure',
        'flow_rate_at_test_buttom_hole_pressure',
        'gas_composition',
        'gas_oil_ratio',
        'gas_specific_gravity',
        'gas_viscosity',
        'oil_composition',
        'oil_gravity',
        'oil_specific_gravity',
        'oil_viscosity',
        'saturate_pressure',
        'static_buttom_hole_pressure',
        'test_buttom_hole_pressure',
        'total_flow_rate',
        'water_cut',
        'water_salinity',
        'water_specific_gravity',
        # Gas Impurities
        'co2',
        'h2s',
        'n2',
        # Correlations
        'bubble_point_pressure_correlation_option',
        'oil_gravity_correlation_option',
        'gas_impurities_correlation_option',
        'gas_oil_ratio_correlation_option',
        'gas_specific_gravity_correlation_option',
        'oil_gravity_correlation_option',
        'water_cut_correlation_option',
        'water_specific_gravity_correlation_option',
        ### Separator Model
        'depth_of_separator_installation',
        # Separator Related
        'gas_density',
        'oil_api',
        'water_density',
        'water_viscosity',
        # Pump Related
        "gor_at_pump_inlet",
        "oil_bubble_point_pressure_at_inlet",
        "oil_density_at_pump_inlet",
        "oil_pressure_at_pump_inlet",
        "oil_temperature_at_pump_inlet",
        "wellhead_pressure",
    ]


class ReservoirPanelForm(forms.Form):

    flow_rate_vs_pressure = forms.FloatField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInput(
            attrs={
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'required': 'required',
            }
        )
    )

    reservoir_pressure = forms.FloatField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                'units': convert.target_units('reservoir_pressure'),
                'target_unit': convert.target_unit('reservoir_pressure'),
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'required': 'required',
            }
        ),
    )

    reservoir_temperature = forms.FloatField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                # 'label': 'Bubble Point Pressure'

                'units': convert.target_units('reservoir_temperature'),
                'target_unit': convert.target_unit('reservoir_temperature'),
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'placeholder': 'reservoir temperature',
                'tooltip': 'please enter reservoir temperature value',
                'required': 'required',
            }
        ),
    )

    reservoir_type_option = forms.CharField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=Dropdown(
            attrs={
                'required': 'required',
                'label': 'Reservoir Type',
                'place_holder': 'reservoir type',
            },
            choices=(
                (option.value, option.display_name) for option in
                            Option.objects.filter(field_name='reservoir_type_option')
            )
        ),
    )

    field_order = [
        ### Reservoir Model
        # General Fields
        'flow_rate_vs_pressure',
        'reservoir_pressure',
        'reservoir_temperature',
        'reservoir_type_option',
    ]


class WellPanelForm(forms.Form):
    separator_temperature = forms.FloatField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                # 'label': 'Bubble Point Pressure'
                'units': convert.target_units('bubble_point_pressure'),
                'target_unit': convert.target_unit('bubble_point_pressure'),
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'placeholder': 'bubble point pressure',
                'tooltip': 'please enter bubble point pressure value',
                'required': 'required',
            }
        ),
    )

    separator_pressure = forms.FloatField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                # 'label': 'Bubble Point Pressure'
                'units': convert.target_units('bubble_point_pressure'),
                'target_unit': convert.target_unit('bubble_point_pressure'),
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'placeholder': 'separator pressure',
                'tooltip': 'please enter separator pressure value',
                'required': 'required',
            }
        ),
    )

    tubing_inside_Dia = forms.FloatField()

    tubing_outside_diameter = forms.FloatField()

    casing_outside_diameter = forms.FloatField()

    casing_inside_diameter = forms.FloatField()

    wellhead_temperature = forms.FloatField()

    well_measured_depth = forms.FloatField()

    tubing_elasticity = forms.FloatField()

    weight_perunit_lenghthfor_tubing = forms.FloatField()

    tubing_thickness = forms.FloatField()

    pump_unit_dimension = forms.FloatField()

    h_size = forms.FloatField()

    pump_unit_weight = forms.FloatField()

    stroke_length = forms.FloatField()

    sprockets_diameter = forms.FloatField()

    total_counterweight = forms.FloatField()

    auxiliary_counterweight = forms.FloatField()

    load_belt_width = forms.FloatField()

    load_belt_length = forms.FloatField()

    load_belt_tensile_strength = forms.FloatField()

    chain_length = forms.FloatField()

    chain_pitch_size = forms.FloatField()

    chain_tensile_strength = forms.FloatField()

    plunger_dia = forms.FloatField()

    plunger_weight = forms.FloatField()

    plunger_friction_force = forms.FloatField()

    standing_valve_opening_delta_p = forms.FloatField()

    traveling_valve_opening_delta_p = forms.FloatField()

    pump_efficiency = forms.FloatField()

    gear_reducer_ratio = forms.FloatField()

    gear_reducer_rating = forms.FloatField()

    pulley_ratio = forms.FloatField()

    small_pulley_size = forms.FloatField()

    large_pulley_size = forms.FloatField()

    pulley_groove_number = forms.FloatField()

    pulley_belt_type = forms.CharField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=Dropdown(
            attrs={
                'required': 'required',
            },
            choices=(
                (option.value, option.display_name) for option in
                Option.objects.filter(field_name='pulley_belt_type')
            )
        )
    )

    user_defined_pump_unit = forms.CharField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=Dropdown(
            attrs={
                'required': 'required',
            },
            choices=(
                (option.value, option.display_name) for option in
                Option.objects.filter(field_name='user_defined_pump_unit')
            )
        )
    )

    well_type = forms.CharField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=Dropdown(
            attrs={
                'required': 'required',
            },
            choices=(
                (option.value, option.display_name) for option in
                Option.objects.filter(field_name='well_type')
            )
        )
    )


class SeparatorPanelForm(forms.Form):
    input_pressure_drop = forms.FloatField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                # 'label': 'Bubble Point Pressure'
                # 'units': convert.target_units('power'),
                # 'target_unit': convert.target_unit('power'),
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'placeholder': 'input pressure droph',
                'tooltip': 'please enter input pressure drop value',
                'required': 'required',
            }
        )
    )

    input_efficiency = forms.FloatField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                # 'label': 'Bubble Point Pressure'
                # 'units': convert.target_units('power'),
                # 'target_unit': convert.target_unit('power'),
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'placeholder': 'input efficiency',
                'tooltip': 'please enter input efficiency value',
                'required': 'required',
            }
        )
    )

    length = forms.FloatField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                # 'label': 'Bubble Point Pressure'
                # 'units': convert.target_units('power'),
                # 'target_unit': convert.target_unit('power'),
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'placeholder': 'length',
                'tooltip': 'please enter length value',
                'required': 'required',
            }
        )
    )


class PumpPanelForm(forms.Form):
    pump_depth = forms.FloatField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                # 'label': 'Bubble Point Pressure'
                # 'units': convert.target_units('power'),
                # 'target_unit': convert.target_unit('power'),
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'placeholder': 'pump depth',
                'tooltip': 'please enter pump depth value',
                'required': 'required',
            }
        )
    )
	
    field_order = [
        "pump_depth"
    ]


class RodPanelForm(forms.Form):
    rods_dia = forms.FloatField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                # 'label': 'Bubble Point Pressure'
                # 'units': convert.target_units('power'),
                # 'target_unit': convert.target_unit('power'),
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'placeholder': 'rods dia',
                'tooltip': 'please enter rods dia value',
                'required': 'required',
            }
        )
    )

    elasticity = forms.FloatField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                # 'label': 'Bubble Point Pressure'
                # 'units': convert.target_units('power'),
                # 'target_unit': convert.target_unit('power'),
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'placeholder': 'elasticity',
                'tooltip': 'please enter elasticity value',
                'required': 'required',
            }
        )
    )

    string_length = forms.FloatField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                # 'label': 'Bubble Point Pressure'
                # 'units': convert.target_units('power'),
                # 'target_unit': convert.target_unit('power'),
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'placeholder': 'string length',
                'tooltip': 'please enter string length value',
                'required': 'required',
            }
        )
    )

    weight_per_unit_Length = forms.FloatField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                # 'label': 'Bubble Point Pressure'
                # 'units': convert.target_units('power'),
                # 'target_unit': convert.target_unit('power'),
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'placeholder': 'weight per unit Length',
                'tooltip': 'please enter weight per unit Length value',
                'required': 'required',
            }
        )
    )

    polished_rod_friction_force = forms.FloatField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                # 'label': 'Bubble Point Pressure'
                # 'units': convert.target_units('power'),
                # 'target_unit': convert.target_unit('power'),
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'placeholder': 'polished rod friction force',
                'tooltip': 'please enter polished rod friction force value',
                'required': 'required',
            }
        )
    )
	
    field_order = [
        "rods_dia",
        "elasticity",
        "string_length",
        "weight_per_unit_Length",
        "polished_rod_friction_force",
    ]


class PumpUnitFormPanel(forms.Form):
    Kinematics_for_Polished_rods = forms.FloatField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                # 'label': 'Bubble Point Pressure'
                # 'units': convert.target_units('power'),
                # 'target_unit': convert.target_unit('power'),
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'placeholder': 'Kinematics for Polished rods',
                'tooltip': 'please enter Kinematics for Polished rods value',
                'required': 'required',
            }
        )
    )
	
    field_order = [
        "Kinematics_for_Polished_rods"
    ]


class GearBoxFormPanel(forms.Form):
    power = forms.FloatField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                # 'label': 'Bubble Point Pressure'
                # 'units': convert.target_units('power'),
                # 'target_unit': convert.target_unit('power'),
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'placeholder': 'power',
                'tooltip': 'please enter power value',
                'required': 'required',
            }
        )
    )
    speed_revolution = forms.FloatField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                # 'label': 'Bubble Point Pressure'
                # 'units': convert.target_units('speed_revolution'),
                # 'target_unit': convert.target_unit('speed_revolution'),
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'placeholder': 'speed revolution',
                'tooltip': 'please enter speed revolution value',
                'required': 'required',
            }
        )
    )

    reduction_ratio = forms.FloatField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInput(
            attrs={
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'required': 'required',
            }
        )
    )

    Diameter = forms.FloatField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                # 'label': 'Bubble Point Pressure'
                # 'units': convert.target_units('speed_revolution'),
                # 'target_unit': convert.target_unit('speed_revolution'),
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'placeholder': 'diameter',
                'tooltip': 'please enter diameter value',
                'required': 'required',
            }
        )
    )

    poisson_ratio = forms.FloatField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInput(
            attrs={
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'required': 'required',
            }
        )
    )
    young_modulus = forms.FloatField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                # 'label': 'Bubble Point Pressure'
                # 'units': convert.target_units('speed_revolution'),
                # 'target_unit': convert.target_unit('speed_revolution'),
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'placeholder': 'young modulus',
                'tooltip': 'please enter young modulus value',
                'required': 'required',
            }
        )
    )

    hardness = forms.FloatField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                # 'label': 'Bubble Point Pressure'
                # 'units': convert.target_units('speed_revolution'),
                # 'target_unit': convert.target_unit('speed_revolution'),
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'placeholder': 'hardness',
                'tooltip': 'please enter hardness value',
                'required': 'required',
            }
        )
    )

    reliability = forms.FloatField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                # 'label': 'Bubble Point Pressure'
                # 'units': convert.target_units('speed_revolution'),
                # 'target_unit': convert.target_unit('speed_revolution'),
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'placeholder': 'reliability',
                'tooltip': 'please enter reliability value',
                'required': 'required',
            }
        )
    )

    normal_module = forms.FloatField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                # 'label': 'Bubble Point Pressure'
                # 'units': convert.target_units('speed_revolution'),
                # 'target_unit': convert.target_unit('speed_revolution'),
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'placeholder': 'normal module',
                'tooltip': 'please enter normal module value',
                'required': 'required',
            }
        )
    )

    Width = forms.FloatField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                # 'label': 'Bubble Point Pressure'
                # 'units': convert.target_units('speed_revolution'),
                # 'target_unit': convert.target_unit('speed_revolution'),
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'placeholder': 'power',
                'tooltip': 'please enter width value',
                'required': 'required',
            }
        )
    )

    normal_pressure_angle = forms.FloatField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                # 'label': 'Bubble Point Pressure'
                # 'units': convert.target_units('speed_revolution'),
                # 'target_unit': convert.target_unit('speed_revolution'),
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'placeholder': 'normal pressure angle',
                'tooltip': 'please enter normal pressure angle value',
                'required': 'required',
            }
        )
    )

    helix_angle = forms.FloatField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                # 'label': 'Bubble Point Pressure'
                # 'units': convert.target_units('speed_revolution'),
                # 'target_unit': convert.target_unit('speed_revolution'),
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'placeholder': 'helix angle',
                'tooltip': 'please enter helix angle value',
                'required': 'required',
            }
        )
    )

    accuracy_grade_number = forms.FloatField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInput(
            attrs={
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'required': 'required',
            }
        )
    )

    depth_situation = forms.FloatField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInput(
            attrs={
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'required': 'required',
            }
        )
    )

    working_lifetime = forms.FloatField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                # 'label': 'Bubble Point Pressure'
                # 'units': convert.target_units('speed_revolution'),
                # 'target_unit': convert.target_unit('speed_revolution'),
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'placeholder': 'working lifetime',
                'tooltip': 'please enter working lifetime value',
                'required': 'required',
            }
        )
    )

    total_distance_between_two_bearing = forms.FloatField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                # 'label': 'Bubble Point Pressure'
                # 'units': convert.target_units('speed_revolution'),
                # 'target_unit': convert.target_unit('speed_revolution'),
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'placeholder': 'total distance between two bearing',
                'tooltip': 'please enter total distance between two bearing value',
                'required': 'required',
            }
        )
    )

    distance_between_pair_gears_andmiddle_of_shaft = forms.FloatField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                # 'label': 'Bubble Point Pressure'
                # 'units': convert.target_units('speed_revolution'),
                # 'target_unit': convert.target_unit('speed_revolution'),
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'placeholder': 'distance between pair gears andmiddle of shaft',
                'tooltip': 'please enter distance between pair gears andmiddle of shaft value',
                'required': 'required',
            }
        )
    )

    Safety_factor = forms.FloatField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInput(
            attrs={
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'required': 'required',
            }
        )
    )

    ultimate_strength = forms.FloatField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                # 'label': 'Bubble Point Pressure'
                # 'units': convert.target_units('speed_revolution'),
                # 'target_unit': convert.target_unit('speed_revolution'),
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'placeholder': 'ultimate strength',
                'tooltip': 'please enter ultimate strength value',
                'required': 'required',
            }
        )
    )

    yield_strength = forms.FloatField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                # 'label': 'Bubble Point Pressure'
                # 'units': convert.target_units('speed_revolution'),
                # 'target_unit': convert.target_unit('speed_revolution'),
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'placeholder': 'yield strength',
                'tooltip': 'please enter yield strength value',
                'required': 'required',
            }
        )
    )

    alternating_bending_moment = forms.FloatField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                # 'label': 'Bubble Point Pressure'
                # 'units': convert.target_units('speed_revolution'),
                # 'target_unit': convert.target_unit('speed_revolution'),
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'placeholder': 'alternating bending moment',
                'tooltip': 'please enter alternating bending moment value',
                'required': 'required',
            }
        )
    )

    midrange_bending_moment = forms.FloatField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                # 'label': 'Bubble Point Pressure'
                # 'units': convert.target_units('speed_revolution'),
                # 'target_unit': convert.target_unit('speed_revolution'),
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'placeholder': 'midrange bending moment',
                'tooltip': 'please enter midrange bending moment value',
                'required': 'required',
            }
        )
    )

    midrange_torque = forms.FloatField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                # 'label': 'Bubble Point Pressure'
                # 'units': convert.target_units('speed_revolution'),
                # 'target_unit': convert.target_unit('speed_revolution'),
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'placeholder': 'midrange torque',
                'tooltip': 'please enter midrange torque value',
                'required': 'required',
            }
        )
    )

    alternating_torque = forms.FloatField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                # 'label': 'Bubble Point Pressure'
                # 'units': convert.target_units('speed_revolution'),
                # 'target_unit': convert.target_unit('speed_revolution'),
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'placeholder': 'alternating torque',
                'tooltip': 'please enter alternating torque value',
                'required': 'required',
            }
        )
    )

    working_temp = forms.FloatField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                # 'label': 'Bubble Point Pressure'
                # 'units': convert.target_units('speed_revolution'),
                # 'target_unit': convert.target_unit('speed_revolution'),
                # 'min': 1,
                # 'max': 39,
                'step': 0.1,
                'placeholder': 'working temp',
                'tooltip': 'please enter working temp value',
                'required': 'required',
            }
        )
    )

    shaft_surface_finish = forms.CharField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=Dropdown(
            attrs={
                'required': 'required',
            },
            choices=(
                (option.value, option.display_name) for option in
                Option.objects.filter(field_name='shaft_surface_finish')
            )
        )
    )

    coating = forms.CharField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=Dropdown(
            attrs={
                'required': 'required',
            },
            choices=(
                (option.value, option.display_name) for option in
                Option.objects.filter(field_name='coating')
            )
        )
    )

    theory_for_calculatio_th_shaft_dia = forms.CharField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=Dropdown(
            attrs={
                'required': 'required',
            },
            choices=(
                (option.value, option.display_name) for option in
                Option.objects.filter(field_name='theory_for_calculatio_th_shaft_dia')
            )
        )
    )

    Driving_working_characteristics_of_the_driving_machine = forms.CharField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=Dropdown(
            attrs={
                'required': 'required',
            },
            choices=(
                (option.value, option.display_name) for option in
                Option.objects.filter(field_name='Driving_working_characteristics_of_the_driving_machine')
            )
        )
    )

    driven_working_characteristics_of_the_driven_machine = forms.CharField(
        error_messages={
            # "min_value": "Value must be greater than 1",
            # "max_value": "Value must be equal or less than 39",
            "required": "Please fill out this field",
        },
        widget=Dropdown(
            attrs={
                'required': 'required',
            },
            choices=(
                (option.value, option.display_name) for option in
                Option.objects.filter(field_name='driven_working_characteristics_of_the_driven_machine')
            )
        )
    )
	
    field_order = [
        "power",
        "speed_revolution",
        "reduction_ratio",
        "Diameter",
        "poisson_ratio",
        "young_modulus",
        "hardness",
        "reliability",
        "normal_module",
        "Width",
        "normal_pressure_angle",
        "helix_angle",
        "accuracy_grade_number",
        "depth_situation",
        "working_lifetime",
        "total_distance_between_two_bearing",
        "distance_between_pair_gears_andmiddle_of_shaft",
        "Safety_factor",
        "ultimate_strength",
        "yield_strength",
        "alternating_bending_moment",
        "midrange_bending_moment",
        "midrange_torque",
        "alternating_torque",
        "working_temp",
        "shaft_surface_finish",
        "coating",
        "theory_for_calculatio_th_shaft_dia",
        "Driving_working_characteristics_of_the_driving_machine",
        "driven_working_characteristics_of_the_driven_machine",
    ]


class MotorPanelForm(forms.Form):
    power_factor = forms.FloatField(
        min_value=0,
        max_value=1,
        error_messages={
            "min_value": "Value must be greater than 0",
            "max_value": "Value must be equal or less than 1",
            "required": "Please fill out this field",
        },
        widget=NumberInputWithUnit(
            attrs={
                # 'label': 'Bubble Point Pressure'
                # 'units': convert.target_units('power_factor'),
                # 'target_unit': convert.target_unit('power_factor'),
                'min': 0,
                'max': 1,
                'step': 0.1,
                'placeholder': 'power factor',
                'tooltip': 'please enter power factor value',
                'required': 'required',
            }
        )
    )
	
    field_order = [
        "power_factor"
    ]


from .models import ExcelTestModel

class ExcelForm(forms.ModelForm):
    class Meta:
        model = ExcelTestModel
        fields = ['name']

    name = forms.CharField(
        max_length=1,
        error_messages={
            'max_length': "Max length.",
        }

    )






