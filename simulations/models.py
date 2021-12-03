from django.db import models
from django.conf import settings
from datetime import datetime
# from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from main.models import Role, Option


class Simulation(models.Model):
    class SimulationState(models.IntegerChoices):
        Initial = 1
        Fluid = 2
        IPR = 3
        Well = 4
        Separator = 5
        Rod = 6
        PumpUnit = 7
        SurfaceEquipment = 8

    class SimulationVisibility(models.IntegerChoices):
        Private = 1
        Public = 2

    name = models.CharField(max_length=50)
    url = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=500, default=None, blank=True, null=True)
    visibility = models.IntegerField(choices=SimulationVisibility.choices, default=1)
    state = models.IntegerField(choices=SimulationState.choices, default=1)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Membership')

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def has_fluid(self):
        exist = False
        try:
            exist = (self.fluid is not None)
        except Fluid.DoesNotExist:
            pass
        return exist

    def has_reservoir(self):
        exist = False
        try:
            exist = (self.reservoir is not None)
        except Reservoir.DoesNotExist:
            pass
        return exist

    def has_ipr(self):
        exist = False
        try:
            exist = (self.ipr is not None)
        except IPR.DoesNotExist:
            pass
        return exist

    def has_well(self):
        exist = False
        try:
            exist = (self.well is not None)
        except Well.DoesNotExist:
            pass
        return exist

    def has_separator(self):
        exist = False
        try:
            exist = (self.separator is not None)
        except Separator.DoesNotExist:
            pass
        return exist

    def has_rod(self):
        exist = False
        try:
            exist = (self.rod is not None)
        except Rod.DoesNotExist:
            pass
        return exist

    def has_pumpunit(self):
        exist = False
        try:
            exist = (self.pumpunit is not None)
        except PumpUnit.DoesNotExist:
            pass
        return exist


class Membership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    is_user_creator = models.BooleanField(default=False)
    role = models.ForeignKey(Role, null=True, on_delete=models.SET_NULL)
    simulation = models.ForeignKey(Simulation, null=True, on_delete=models.SET_NULL)
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Fluid(models.Model):

    @classmethod
    def fields(cls):
        return [f.name for f in cls._meta.fields + cls._meta.many_to_many]

    ### Inputs
    # General Fields
    production_gor = models.FloatField(null=True, blank=True)
    bubble_point_pressure = models.FloatField(null=True, blank=True)  # also Output
    flow_rate_at_test_buttom_hole_pressure = models.FloatField(null=True, blank=True)
    gas_composition = models.FloatField(null=True, blank=True)
    gas_oil_ratio = models.FloatField(null=True, blank=True)  # also Output
    gas_specific_gravity = models.FloatField(null=True, blank=True)
    # gas_viscosity = models.FloatField(null=True, blank=True)
    oil_composition = models.FloatField(null=True, blank=True)
    oil_gravity = models.FloatField(null=True, blank=True)
    oil_specific_gravity = models.FloatField(null=True, blank=True)
    oil_viscosity = models.FloatField(null=True, blank=True)  # also Output
    oil_compressibility = models.FloatField(null=True, blank=True)
    oil_formation_volume_factor = models.FloatField(null=True, blank=True)
    saturate_pressure = models.FloatField(null=True, blank=True)
    static_buttom_hole_pressure = models.FloatField(null=True, blank=True)
    test_buttom_hole_pressure = models.FloatField(null=True, blank=True)
    total_flow_rate = models.FloatField(null=True, blank=True)
    water_cut = models.FloatField(null=True, blank=True)
    water_salinity = models.FloatField(null=True, blank=True)
    water_specific_gravity = models.FloatField(null=True, blank=True)
    # Gas Impurities
    co2 = models.FloatField(null=True, blank=True)
    h2s = models.FloatField(null=True, blank=True)
    n2 = models.FloatField(null=True, blank=True)
    undersaturated_oil_viscosity = models.CharField(max_length=255, null=True, blank=True)
    solution_gas_oil_ratio_correlation = models.CharField(max_length=255)
    Oil_FVF = models.CharField(max_length=255)
    gas_SP_GR = models.FloatField()
    water_SP_GR = models.FloatField()


    # Seperateor condition
    tempreture = models.FloatField()
    pressure = models.FloatField()

    # Correlations
    solution_GOR = models.ForeignKey(Option,
                                                     related_name='solution_GOR', null=True,
                                                     on_delete=models.SET_NULL)

    gas_viscosity_correlation = models.ForeignKey(Option,
                                                     related_name='gas_viscosity_correlation', null=True,
                                                     on_delete=models.SET_NULL)

    bubble_point_pressure_correlation_option = models.ForeignKey(Option,
                                                                 related_name='fluids_by_bubble_point_pressure_correlation_option',
                                                                 null=True, on_delete=models.SET_NULL)
    oil_gravity_correlation_option = models.ForeignKey(Option,
                                                       related_name='fluids_by_oil_gravity_correlation_option',
                                                       null=True,
                                                       on_delete=models.SET_NULL)
    gas_impurities_correlation_option = models.ForeignKey(Option,
                                                          related_name='fluids_by_gas_impurities_correlation_option'
                                                          , null=True, on_delete=models.SET_NULL)
    gas_oil_ratio_correlation_option = models.ForeignKey(Option,
                                                         related_name='fluids_by_gas_oil_ratio_correlation_option',
                                                         null=True,
                                                         on_delete=models.SET_NULL)
    gas_specific_gravity_correlation_option = models.ForeignKey(Option,
                                                                related_name='fluids_by_gas_specific_gravity_correlation_option'
                                                                , null=True, on_delete=models.SET_NULL)

    water_cut_correlation_option = models.ForeignKey(Option,
                                                     related_name='water_cut_correlation_option', null=True,
                                                     on_delete=models.SET_NULL)
    water_specific_gravity_correlation_option = models.ForeignKey(Option,
                                                                  related_name='fluids_by_water_specific_gravity_correlation_option'
                                                                  , null=True, on_delete=models.SET_NULL)

    dead_oil_viscosity_correlation = models.CharField(max_length=255, null=True, blank=True)
    saturated_oil_viscosity_correlations = models.CharField(max_length=255, null=True, blank=True)

    # Separator Related
    gas_density = models.FloatField(null=True, blank=True)
    oil_api = models.FloatField(null=True, blank=True)
    water_density = models.FloatField(null=True, blank=True)
    water_viscosity = models.FloatField(null=True, blank=True)
    # Pump Related
    gor_at_pump_inlet = models.FloatField(null=True, blank=True)
    oil_bubble_point_pressure_at_inlet = models.FloatField(null=True, blank=True)
    oil_density_at_pump_inlet = models.FloatField(null=True, blank=True)
    oil_pressure_at_pump_inlet = models.FloatField(null=True, blank=True)
    oil_temperature_at_pump_inlet = models.FloatField(null=True, blank=True)
    wellhead_pressure = models.FloatField(null=True, blank=True)
    # Well Panel
    flow_rate = models.FloatField(null=True, blank=True)
    separator_inlet_temperature = models.FloatField(null=True, blank=True)
    separator_temperature = models.FloatField(null=True, blank=True)
    separator_pressure = models.FloatField(null=True, blank=True)

    ### Outputs
    # General Fields
    free_gas_at_pump_depth = models.FloatField(null=True, blank=True)
    oil_density = models.FloatField(null=True, blank=True)
    volumetric_coefficient = models.FloatField(null=True, blank=True)
    # Correlations
    free_gas_at_pump_depth_correlation_option = models.ForeignKey(Option,
                                                                  related_name='fluids_by_free_gas_at_pump_depth_correlation_option',
                                                                  null=True, on_delete=models.SET_NULL)
    # Pump Related
    oil_production_flow_rate = models.FloatField(null=True, blank=True)

    # The Parent Simulation
    simulation = models.OneToOneField(
        Simulation,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Reservoir(models.Model):

    @classmethod
    def fields(cls):
        return [f.name for f in cls._meta.fields + cls._meta.many_to_many]

    ### Inputs
    # General Fields
    acentric_factors = models.FloatField(null=True, blank=True)
    flow_rate_vs_pressure = models.FloatField(null=True, blank=True)
    productivity_index = models.FloatField(null=True, blank=True)
    reservoir_pressure = models.FloatField(null=True, blank=True)
    reservoir_temperature = models.FloatField(null=True, blank=True)
    reservoir_type_option = models.ForeignKey(Option,
                                              related_name='reservoirs_by_reservoir_type_option',
                                              null=True, on_delete=models.SET_NULL)

    # Type of this item isnt not defined in the excel docs
    # ReservoirFormula

    # The Parent Simulation
    simulation = models.OneToOneField(
        Simulation,
        on_delete=models.CASCADE,
        primary_key=True,
        default=0
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Well(models.Model):

    @classmethod
    def fields(cls):
        return [f.name for f in cls._meta.fields + cls._meta.many_to_many]

    tubing_inside_Dia = models.FloatField(null=True, blank=True)
    tubing_thickness = models.FloatField(null=True, blank=True)
    weight_perunit_lenghthfor_tubing = models.FloatField(null=True, blank=True)
    tubing_elasticity = models.FloatField(null=True, blank=True)
    wellhead_temperature = models.FloatField(null=True, blank=True)
    well_type = models.CharField(max_length=1000, null=True, blank=True)
    well_measured_depth = models.FloatField(null=True, blank=True)
    test_buttom_hole_pressure = models.FloatField(null=True, blank=True)
    flow_rate_at_test_buttom_hole_pressure = models.FloatField(null=True, blank=True)
    water_cut = models.FloatField(null=True, blank=True)
    static_buttom_hole_pressure = models.FloatField(null=True, blank=True)
    casing_outside_diameter = models.FloatField(null=True, blank=True)
    casing_inside_diameter = models.FloatField(null=True, blank=True)
    tubing_outside_diameter = models.FloatField(null=True, blank=True)

    # Down Hole Pressure
    # Is It The Same As IPR.static_bottom_hole_pressure ??
    down_hole_pressure = models.FloatField(null=True, blank=True)
    # Productivity Flow Rate
    productivity_flow_rate = models.FloatField(null=True, blank=True)
    # The Parent Simulation
    simulation = models.OneToOneField(
        Simulation,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Pump(models.Model):

    @classmethod
    def fields(cls):
        return [f.name for f in cls._meta.fields + cls._meta.many_to_many]

    plunger_dia = models.FloatField(null=True, blank=True)
    plunger_weight = models.FloatField(null=True, blank=True)
    plunger_friction_force = models.FloatField(null=True, blank=True)
    standing_valve_opening_delta_p = models.FloatField(null=True, blank=True)
    traveling_valve_opening_delta_p = models.FloatField(null=True, blank=True)
    pump_efficiency = models.FloatField(null=True, blank=True)
    pump_intake_pressure = models.FloatField(null=True, blank=True)
    pump_intake_pressure_correlation_option = models.ForeignKey(Option,
                                                                related_name='pump_intake_pressure_correlation_option',
                                                                null=True,
                                                                on_delete=models.SET_NULL)
    fluid_over_pump = models.FloatField(null=True, blank=True)

    _over_pump_correlation_option = models.ForeignKey(Option,
                                                      related_name='over_pump_correlation_option', null=True,
                                                      on_delete=models.SET_NULL)
    fluid_level = models.FloatField(null=True, blank=True)
    fluid_level_correlation_option = models.ForeignKey(Option,
                                                       related_name='fluid_level_correlation_option', null=True,
                                                       on_delete=models.SET_NULL)
    total_dynamic_head = models.FloatField(null=True, blank=True)
    total_dynamic_head_correlation_option = models.ForeignKey(Option,
                                                              related_name='total_dynamic_head_correlation_option',
                                                              null=True,
                                                              on_delete=models.SET_NULL)
    pump_depth = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class IPR(models.Model):

    @classmethod
    def fields(cls):
        return [f.name for f in cls._meta.fields + cls._meta.many_to_many]

    # Static Bottom Hole Pressure (SBHP)
    static_bottom_hole_pressure = models.FloatField(null=True, blank=True)
    # Fluid Rate at Test Pressure
    fluid_rate_at_test_pressure = models.FloatField(null=True, blank=True)
    # Test Bottom Hole Pressure
    test_bottom_hole_pressure = models.FloatField(null=True, blank=True)
    # Productivity Index
    productivity_index = models.FloatField(null=True, blank=True)
    # IPR Method
    ipr_method = models.ForeignKey(Option, null=True, on_delete=models.SET_NULL)

    water_cut = models.FloatField(null=True, blank=True)

    # The Parent Simulation
    simulation = models.OneToOneField(
        Simulation,
        on_delete=models.CASCADE,
        primary_key=True,
    )  # models.ForeignKey(Simulation, on_delete=models.CASCADE)
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SeparatorSize(models.Model):

    @classmethod
    def fields(cls):
        return [f.name for f in cls._meta.fields + cls._meta.many_to_many]

    # Display Name Of The Separator Size, For Example Large
    display_name = models.CharField(max_length=50)


class Separator(models.Model):

    @classmethod
    def fields(cls):
        return [f.name for f in cls._meta.fields + cls._meta.many_to_many]

    depth_of_separator_installation = models.FloatField(null=True, blank=True)

    separator_temperature = models.FloatField(null=True, blank=True)
    separator_pressure = models.FloatField(null=True, blank=True)
    separator_efficiency = models.FloatField(null=True, blank=True)
    # Separators Sizes, Should Be Selected Of A List
    size_1 = models.ForeignKey(SeparatorSize, related_name='separator_b_size1', null=True, on_delete=models.SET_NULL)
    size_2 = models.ForeignKey(SeparatorSize, related_name='separator_b_size2', null=True, on_delete=models.SET_NULL)
    size_3 = models.ForeignKey(SeparatorSize, related_name='separator_b_size3', null=True, on_delete=models.SET_NULL)
    # Separator Length
    length = models.FloatField(null=True, blank=True)
    # Pressure Drop Along Separator
    input_pressure_drop = models.FloatField(null=True, blank=True)
    # Separator Efficiency
    input_efficiency = models.FloatField(null=True, blank=True)

    # Outputs
    output_flow_rate = models.FloatField(null=True, blank=True)
    # Output Pressure Drop
    output_pressure_drop = models.FloatField(null=True, blank=True)
    # Outlet GOR
    outlet_gor = models.FloatField(null=True, blank=True)
    # Output Efficiency
    output_efficiency = models.FloatField(null=True, blank=True)
    # The Parent Simulation
    simulation = models.OneToOneField(
        Simulation,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Rod(models.Model):

    @classmethod
    def fields(cls):
        return [f.name for f in cls._meta.fields + cls._meta.many_to_many]

    rods_dia = models.FloatField(null=True, blank=True)

    weight_per_unit_Length = models.FloatField(null=True, blank=True)
    elasticity = models.FloatField(null=True, blank=True)
    Kinematics_for_Polished_rods = models.FloatField(null=True, blank=True)

    polished_rod_friction_force = models.FloatField(null=True, blank=True)
    kinematics_for_polished_rod = models.FloatField(null=True, blank=True)

    # Rod String Length
    string_length = models.FloatField(null=True, blank=True)
    # Tubing Diameter
    tubing_diameter = models.FloatField(null=True, blank=True)

    # Outputs
    # output_flow_rate = models.FloatField(null=True, blank=True)

    simulation = models.OneToOneField(
        Simulation,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PumpUnit(models.Model):

    @classmethod
    def fields(cls):
        return [f.name for f in cls._meta.fields + cls._meta.many_to_many]

    user_defined_pump_unit = models.ForeignKey(Option, on_delete=models.CASCADE)
    pump_unit_dimension = models.FloatField(null=False, blank=False)
    h_size = models.FloatField(null=False, blank=False)
    pump_unit_weight = models.FloatField(null=False, blank=False)
    stroke_length = models.FloatField(null=False, blank=False)
    sprockets_diameter = models.FloatField(null=False, blank=False)
    total_counterweight = models.FloatField(null=False, blank=False)
    auxiliary_counterweight = models.FloatField(null=False, blank=False)
    load_belt_width = models.FloatField(null=False, blank=False)
    load_belt_length = models.FloatField(null=False, blank=False)
    load_belt_tensile_strength = models.FloatField(null=False, blank=False)
    chain_length = models.FloatField(null=False, blank=False)
    chain_pitch_size = models.FloatField(null=False, blank=False)
    chain_tensile_strength = models.FloatField(null=False, blank=False)

    # Pump Efficiency
    efficiency = models.FloatField(null=True, blank=True)
    # Pumping Speed
    speed = models.FloatField(null=True, blank=True)

    # Outputs
    # output_flow_rate = models.FloatField(null=True, blank=True)

    simulation = models.OneToOneField(
        Simulation,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Gearbox(models.Model):

    @classmethod
    def fields(cls):
        return [f.name for f in cls._meta.fields + cls._meta.many_to_many]

    gear_reducer_ratio = models.FloatField(null=True, blank=True)
    gear_reducer_rating = models.FloatField(null=True, blank=True)
    pulley_ratio = models.FloatField(null=True, blank=True)
    small_pulley_size = models.FloatField(null=True, blank=True)
    large_pulley_size = models.FloatField(null=True, blank=True)
    pulley_belt_type = models.ForeignKey(Option, on_delete=models.CASCADE)
    pulley_groove_number = models.FloatField(null=True, blank=True)
    power = models.FloatField(null=True, blank=True)
    speed_revolution = models.FloatField(null=True, blank=True)
    reduction_ratio = models.FloatField(null=True, blank=True)
    Diameter = models.FloatField(null=True, blank=True)
    poisson_ratio = models.FloatField(null=True, blank=True)
    young_modulus = models.FloatField(null=True, blank=True)
    hardness = models.FloatField(null=True, blank=True)
    coating = models.CharField(max_length=1000)
    reliability = models.FloatField(null=True, blank=True)
    normal_module = models.FloatField(null=True, blank=True)
    Width = models.FloatField(null=True, blank=True)
    normal_pressure_angle = models.FloatField(null=True, blank=True)
    helix_angle = models.FloatField(null=True, blank=True)
    accuracy_grade_number = models.FloatField(null=True, blank=True)
    depth_situation = models.FloatField(null=True, blank=True)
    Driving_working_characteristics_of_the_driving_machine = models.CharField(max_length=1000)
    driven_working_characteristics_of_the_driven_machine = models.CharField(max_length=1000)
    working_lifetime = models.FloatField(null=True, blank=True)
    total_distance_between_two_bearing = models.FloatField(null=True, blank=True)
    distance_between_pair_gears_andmiddle_of_shaft = models.FloatField(null=True, blank=True)
    theory_for_calculatio_th_shaft_dia = models.CharField(max_length=1000)
    Safety_factor = models.FloatField(null=True, blank=True)
    ultimate_strength = models.FloatField(null=True, blank=True)
    yield_strength = models.FloatField(null=True, blank=True)
    alternating_bending_moment = models.FloatField(null=True, blank=True)
    midrange_bending_moment = models.FloatField(null=True, blank=True)
    midrange_torque = models.FloatField(null=True, blank=True)
    alternating_torque = models.FloatField(null=True, blank=True)
    working_temp = models.FloatField(null=True, blank=True)
    # Reliability = models.FloatField(null=True, blank=True)
    shaft_surface_finish = models.CharField(max_length=1000)

    # Gear Speed
    speed = models.FloatField(null=True, blank=True)

    # Outputs
    # output_flow_rate = models.FloatField(null=True, blank=True)

    simulation = models.OneToOneField(
        Simulation,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Motor(models.Model):

    @classmethod
    def fields(cls):
        return [f.name for f in cls._meta.fields + cls._meta.many_to_many]

    # Slip
    slip = models.FloatField(null=True, blank=True)
    # Power Factor
    power_factor = models.FloatField(null=True, blank=True)
    # Nominal Voltage
    nominal_voltage = models.ForeignKey(Option,
                                        related_name='motors_by_nominal_voltage_option', null=True,
                                        on_delete=models.SET_NULL)
    # Pole
    pole_option = models.ForeignKey(Option,
                                    related_name='motors_by_pole_option', null=True,
                                    on_delete=models.SET_NULL)
    # Efficiency Classes
    efficiency_classes_option = models.ForeignKey(Option,
                                                  related_name='motors_by_efficiency_classes_option', null=True,
                                                  on_delete=models.SET_NULL)
    # Nominal Frequency
    nominal_frequency_option = models.ForeignKey(Option,
                                                 related_name='motors_by_nominal_frequency_option', null=True,
                                                 on_delete=models.SET_NULL)
    # Synchronous Speed
    synchronous_speed = models.FloatField(null=True, blank=True)
    # Isolation Class
    isolation_class_option = models.ForeignKey(Option,
                                               related_name='motors_by_isolation_class_option', null=True,
                                               on_delete=models.SET_NULL)
    # Duty Cycle
    duty_cycle_option = models.ForeignKey(Option,
                                          related_name='motors_by_duty_cycle_option', null=True,
                                          on_delete=models.SET_NULL)
    # Enclosure Degree Of Protection
    enclosure_degree_of_protection_option = models.ForeignKey(Option,
                                                              related_name='motors_by_enclosure_degree_of_protection_option',
                                                              null=True,
                                                              on_delete=models.SET_NULL)
    # Method Of Cooling
    method_of_cooling_option = models.ForeignKey(Option,
                                                 related_name='motors_by_method_of_cooling_option', null=True,
                                                 on_delete=models.SET_NULL)
    # Connection
    connection_option = models.ForeignKey(Option,
                                          related_name='motors_by_connection_option', null=True,
                                          on_delete=models.SET_NULL)
    # Motor Starting
    motor_starting_option = models.ForeignKey(Option,
                                              related_name='motors_by_motor_starting_option', null=True,
                                              on_delete=models.SET_NULL)
    # Zone
    zone_option = models.ForeignKey(Option,
                                    related_name='motors_by_zone_option', null=True,
                                    on_delete=models.SET_NULL)
    # Number of Phases
    number_of_phases_option = models.ForeignKey(Option,
                                                related_name='motors_by_number_of_phases_option', null=True,
                                                on_delete=models.SET_NULL)
    # Rated Output Power
    rated_output_power_option = models.ForeignKey(Option,
                                                  related_name='motors_by_rated_output_power_option', null=True,
                                                  on_delete=models.SET_NULL)
    # Winding Type
    winding_type_option = models.ForeignKey(Option,
                                            related_name='winding_type_option', null=True,
                                            on_delete=models.SET_NULL)
    # Frame Size
    frame_size_option = models.ForeignKey(Option,
                                          related_name='frame_size_option', null=True,
                                          on_delete=models.SET_NULL)


class Design(models.Model):
    # Inputs
    fluid_rate = models.FloatField(null=True, blank=True)
    pump_depth = models.FloatField(null=True, blank=True)
    tubing_pressure = models.FloatField(null=True, blank=True)
    casing_pressure = models.FloatField(null=True, blank=True)
    # Outputs
    intake_pressure = models.FloatField(null=True, blank=True)
    fluid_over_pump = models.FloatField(null=True, blank=True)
    tdh = models.FloatField(null=True, blank=True)
    free_gas_intake = models.FloatField(null=True, blank=True)

    ##
    pb_depth = models.FloatField(null=True, blank=True)


class WellSchematic(models.Model):
    casing_inside_diameter = models.FloatField(null=True, blank=True)
    casing_outside_Diameter = models.FloatField(null=True, blank=True)
    casing_weight = models.FloatField(null=True, blank=True)
    casing_depth = models.FloatField(null=True, blank=True)
    tubing_inside_diameter = models.FloatField(null=True, blank=True)
    tubing_outside_diameter = models.FloatField(null=True, blank=True)
    tubing_weight = models.FloatField(null=True, blank=True)
    tubing_depth = models.FloatField(null=True, blank=True)
    top_of_perforation = models.FloatField(null=True, blank=True)
    wellbore_correlations = models.FloatField(null=True, blank=True)
    md = models.FloatField(null=True, blank=True)
    tvd = models.FloatField(null=True, blank=True)
    angle = models.FloatField(null=True, blank=True)
    reservoir_temperature = models.FloatField(null=True, blank=True)
    reservoir_pressure = models.FloatField(null=True, blank=True)


class OdWeightId(models.Model):
    outside_diameter_OD = models.FloatField(null=False, blank=False)
    inside_diameter_ID = models.FloatField(null=False, blank=False)
    weight = models.FloatField(null=False, blank=False)

    def __str__(self):
        return str(self.outside_diameter_OD) \
               + "-" + str(self.inside_diameter_ID) \
               + "-" + str(self.weight)


class CasingTubing(models.Model):
    type = models.CharField(max_length=20, null=True, blank=True)
    bottom = models.FloatField(null=True, blank=True)
    top = models.FloatField(null=True, blank=True)
    outside_diameter = models.FloatField(null=True, blank=True)
    inside_diameter = models.FloatField(null=True, blank=True)
    roughness = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.type


class ExcelTestModel(models.Model):
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name + " - " + str(self.age)