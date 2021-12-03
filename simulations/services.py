import abc
from django import forms
from .models import Option, Simulation, Fluid, Reservoir, Well, Pump, IPR, Separator, SeparatorSize, Rod, PumpUnit, Gearbox, Motor
from main.models import Option
from contextlib import contextmanager
from django.db import transaction, DEFAULT_DB_ALIAS
from datetime import datetime
from utils.general_utils import with_keys, without_keys
import copy
from modules.dummy import Core

class Service:

    db_transaction = True
    run_post_process = True
    using = DEFAULT_DB_ALIAS

    def __init__(cls, inputs, *args, **kwargs):
        return None

    @classmethod
    def execute(cls, inputs, *args, **kwargs):
        """
        Function to be called from the outside to kick off the Service
        functionality.
        :param dictionary inputs: data parameters for Service, checked
            against the fields defined on the Service class.
        :param dictionary *args:  any additional parameters Service may
            need, can be an empty dictionary
        :param dictionary **kwargs: any additional parameters Service may
            need, can be an empty dictionary
        """

        instance = cls(inputs, *args, **kwargs)
        # instance.service_clean()
        with instance._process_context():
            return instance.process(inputs, *args, **kwargs)

    @abc.abstractmethod
    def process(self, inputs, *args, **kwargs):
        """
        Main method to be overridden; contains the Business Rules
        functionality.
        """
        pass

    @contextmanager
    def _process_context(self):
        """
        Returns the context for :meth:`process`
        :return:
        """
        if self.db_transaction:
            with transaction.atomic(using=self.using):
                if self.run_post_process:
                    transaction.on_commit(self.post_process)
                yield
        else:
            yield
            if self.run_post_process:
                self.post_process()

    def post_process(self):
        """
        Post process method to be perform extra actions once :meth:`process`
        successfully executes.
        """
        pass

        
    @abc.abstractmethod
    def do_business_logics(inputs=None):
        """
        Main method to be overridden; contains the Business Rules
        functionality.
        """
        pass


class ConvertUnitService:
    
    class Systems:
        DEFAULT = 'default'
        SI = 'SI'


    ###
    # has Conversion
    ###
    # distance
    M = 'm'; FT = 'Ft'; IN = 'in'

    # mass
    KG = 'kg'; LBF = 'lbf'

    # force
    N = 'N'

    # pressure
    KPA ='kpa'; PSI = 'psi'; PSIA = 'psia'; PSIG = 'psig'; ATM = 'atm'; LBF_IN2 = 'lbf/in^2'; PA = 'pa'; LBF_FT2 = 'lbf/ft^2'

    # torque
    NM = 'n*m'; FT_LBF = 'ft*lbf'

    # density
    KG_M3 = 'Kg/m^3'; LBF_FT3 = 'lbf/ft^3' 
    
    # barrel
    M3 = 'm^3'; BBL = 'bbl'
    
    # volumetric flow rate
    M3_S = 'm^3/s'; M3_D = 'm^3/d'; BBL_D = 'bbl/d'; FT3_S = 'ft^3/s'

    # gas-oil ratio
    M3_M3 = 'm^3/m^3'; SCF_BBL = 'Scf/bbl'

    # dynamic viscosity
    PA_S = 'Pa*s'; LB_S_FT2 = 'lb*s/ft2'; CENTIPOISE = 'centipoise'

    # kinematic viscosity
    CM2_S = 'Cm^2/s'; IN2_S = 'In^2/s'; FT2_S = 'Ft^2/s'

    # power
    W = 'W'; BTU_HR = 'BTU/hr'; FT_LB_S = 'ft*lb/s'; HP = 'hp'

    # water-oil ratio

    # velocity
    MS = 'm/s'; FT_S = 'Ft/s'
    
    # acceleration
    M_S2 = 'm/s^2'; FT_S2 = 'ft/s2'; IN_S2 = 'ft/s2' 

    # linear density
    KG_M = 'Kg/m'; LB_FT = 'Lb/ft'

    # temperature
    C = '◦C'; F = '◦F'

    ###
    # hasn't Conversion
    ###
    # API = '°API'
    # CP = 'cp'
    # PSIG = 'psig'

    # Units Coefficient
    units = {
        # distance
        M:1.0, FT:0.3048, IN:0.0254,
        # mass and force
        LBF:1.0, KG:2.2046, N:0.2248,
        # pressure
        KPA:1.0, PSI:6.8947, PSIA:6.8947, PSIG:6.8947, ATM:101.325, LBF_IN2:6.8948, PA:0.001, LBF_FT2:47.88,
        # torque
        NM:1.0, FT_LBF:1.356,
        # density
        KG_M3:1.0, LBF_FT3:16.0184,
        # barrel
        M3:1.0, BBL:159.0,
        # volumetric flow rate
        M3_S:1.0, M3_D:0.000011, BBL_D:0.0000018, FT3_S:0.0283,
        # gas-oil ratio
        M3_M3:1.0, SCF_BBL:5.6145,
        # dynamic viscosity
        PA_S:1.0, LB_S_FT2:0.02089, CENTIPOISE:0.000004,
        # kinematic viscosity
        CM2_S:1.0, IN2_S:6.4516, FT2_S:929.03,
        # power
        W:1.0, BTU_HR:0.2931, FT_LB_S:1.3558, HP:745.7,
        # velocity
        MS:1.0, FT_S:0.3048,
        # acceleration
        M_S2:1.0, FT_S2:0.3048, IN_S2:0.0254,
        # linear density
        KG_M:1.0, LB_FT:1.4882,
        # temperature
        C:1.0, F:1.8,
    }

    def invalid_input_exeption(self, method_name):
        raise ValueError("input was invalid: method {} not found".format(method_name))

    def convert(self, field_name, field_unit, value, system = Systems.DEFAULT):
        """return converted value and target unit

        :param field_name: name of field which needs to be conversion
        :type field_name: str

        :param field_unit: unit of field which needs to be conversion
        :type field_unit: str

        :param value: current value of field which needs to be conversion
        :type value: float

        :param system: system of units (default, SI), defaults to Systems.DEFAULT
        :type system: str, optional

        :return: result of conversion based on current value, unit, requested system and target unit
        :rtype: float
        """    
        target_unit = self.target_unit(field_name, system)
        if field_unit == self.F:
            return (float(value) * self.units[field_unit] / self.units[target_unit])+32, target_unit
        if field_unit == self.C:
            return (float(value) * self.units[field_unit] / self.units[target_unit])-32, target_unit
        
        return float(value) * self.units[field_unit] / self.units[target_unit], target_unit

    def target_unit(self, field_name, system = Systems.DEFAULT):
        """return target unit for requested field based on requested system

        :param field_name: name of field which it's target unit has been requested
        :type field_name: str

        :param system: system of units (default, SI), defaults to Systems.DEFAULT
        :type system: [type], optional

        :return: target unit string
        :rtype: str
        """   
        method_name = system+'_'+field_name+'_target_unit'
        method=getattr(self,method_name,lambda : self.invalid_input_exeption(method_name))
        return method()

    def target_units(self, field_name, system = Systems.DEFAULT):
        """return target units for requested field based on requested system

        :param field_name: name of field which it's target unit has been requested
        :type field_name: str

        :param system: system of units (default, SI), defaults to Systems.DEFAULT
        :type system: [type], optional

        :return: target units list
        :rtype: list
        """   
        method_name = system+'_'+field_name+'_target_units'
        method=getattr(self,method_name,lambda : self.invalid_input_exeption(method_name))
        return method()

    ### Fluid Model
    def default_bubble_point_pressure_target_unit(self):
        return self.PSI
    def default_bubble_point_pressure_target_units(self):
        return [ self.KPA, self.PSI, self.ATM, self.LBF_IN2, self.PA, self.LBF_FT2 ]
    
    def default_flow_rate_at_test_buttom_hole_pressure_target_unit(self):
        return self.BBL_D
    def default_flow_rate_at_test_buttom_hole_pressure_target_units(self):
        return [ self.M3_S, self.M3_D, self.BBL_D, self.FT3_S ]
        
    def default_gas_oil_ratio_target_unit(self):
        return self.SCF_BBL
    def default_gas_oil_ratio_target_units(self):
        return [ self.M3_M3, self.SCF_BBL ]
    
    def default_saturate_pressure_target_unit(self):
        return self.PSI
    def default_saturate_pressure_target_units(self):
        return [ self.KPA, self.PSI, self.ATM, self.LBF_IN2, self.PA, self.LBF_FT2 ]
    
    def default_static_buttom_hole_pressure_target_unit(self):
        return self.PSIG
    def default_static_buttom_hole_pressure_target_units(self):
        return [ self.PSIG ]
        
    def default_test_buttom_hole_pressure_target_unit(self):
        return self.PSIG
    def default_test_buttom_hole_pressure_target_units(self):
        return [ self.PSIG ]
    
    def default_total_flow_rate_target_unit(self):
        return self.BBL_D
    def default_total_flow_rate_target_units(self):
        return [ self.M3_S, self.M3_D, self.BBL_D, self.FT3_S ]
        
    def default_gas_density_target_unit(self):
        return self.KG_M3
    def default_gas_density_target_units(self):
        return [ self.KG_M3, self.LBF_FT3 ]

    def default_water_density_target_unit(self):
        return self.KG_M3
    def default_water_density_target_units(self):
        return [ self.KG_M3, self.LBF_FT3 ]
    
    def default_gor_at_pump_inlet_target_unit(self):
        return self.SCF_BBL
    def default_gor_at_pump_inlet_target_units(self):
        return [ self.M3_M3, self.SCF_BBL ]
    
    def default_oil_bubble_point_pressure_at_inlet_target_unit(self):
        return self.PSI
    def default_oil_bubble_point_pressure_at_inlet_target_units(self):
        return [ self.KPA, self.PSI, self.ATM, self.LBF_IN2, self.PA, self.LBF_FT2 ]
    
    def default_oil_pressure_at_pump_inlet_target_unit(self):
        return self.PSI
    def default_oil_pressure_at_pump_inlet_target_units(self):
        return [ self.KPA, self.PSI, self.ATM, self.LBF_IN2, self.PA, self.LBF_FT2 ]
    
    def default_oil_temperature_at_pump_inlet_target_unit(self):
        return self.F
    def default_oil_temperature_at_pump_inlet_target_units(self):
        return [ self.C, self.F ]
    
    def default_wellhead_pressure_target_unit(self):
        return self.PSI
    def default_wellhead_pressure_target_units(self):
        return [ self.KPA, self.PSI, self.ATM, self.LBF_IN2, self.PA, self.LBF_FT2 ]

    ### Separator Model
    # Fluid Panel
    def default_depth_of_separator_installation_target_unit(self):
        return self.SCF_BBL
    def default_depth_of_separator_installation_target_units(self):
        return [ self.M3_M3, self.SCF_BBL ]
    
    ### Reservoir Model
    def default_reservoir_temperature_target_unit(self):
        return self.F
    def default_reservoir_temperature_target_units(self):
        return [ self.C, self.F ]

    def default_reservoir_pressure_target_unit(self):
        return self.PSI
    def default_reservoir_pressure_target_units(self):
        return [ self.KPA, self.PSI, self.ATM, self.LBF_IN2, self.PA, self.LBF_FT2 ]
    

class DummyModuleService:

    def call_solve_linear_equvations(equations:list):
        # add any business logics here

        return Core.solve_linear_equations(equations)

    def call_calculate(operand1:float, method:str, operand2:float):
        # add any business logics here
        
        return Core.calculate(operand1, method, operand2)

    def call_polynomial_division(dividend_coefficients:list, divisor_coefficients:list):
        # add any business logics here
        
        return Core.polynomial_division(dividend_coefficients, divisor_coefficients)


class UpdateFluidService(Service):
    """This is a Model Service Class use for update a Fluid Model record and
    processing business logics. It is an extended class of the :class:`Service`
    """

    def process(self, inputs, *args, **kwargs):
        """update Fluid record and processing business logics

        :param inputs: fields should to be updated
        :type inputs: dict
        
        :param `*args`: The variable arguments passed to this method

        :param `**kwargs`: The keyword arguments passed to this method

        :return: updated fluid record
        :rtype: :class:`Fluid`
        """
        
        fluid = inputs['fluid']

        # Business Logics Implementation related to the Model
        inputs = self.do_business_logics(inputs)

        # Delete key-value pair which key not in model fields
        # for example csrf token of post request
        inputs = with_keys(inputs, Fluid.fields())

        # Update Fluid record
        fluid = Fluid.objects.update_or_create(
            pk=fluid,
            defaults=inputs,
        )

        return fluid

    def do_business_logics(self, inputs, *args, **kwargs):
        """processing business logics

        :param inputs: fields should to be processed
        :type inputs: dict
        
        :param `*args`: The variable arguments passed to this method

        :param `**kwargs`: The keyword arguments passed to this method

        :return: processed fields
        :rtype: dict
        """      
        
        converter = ConvertUnitService()
        
        for key in inputs:

            # unit conversion for fields which have unit
            if key+'_unit' in inputs:
                value, unit = converter.convert(key, inputs[key+'_unit'], inputs[key])
                inputs[key] = value
                inputs[key+'_unit'] = unit

            # Find Option Objcet fot Correlations fields
            if key.endswith("_option"):
                inputs[key] = Option.objects.filter(field_name=key, value=inputs[key]).first()
            
        return inputs

class CreateFluidService(Service):
    """This is a Model Service Class use for create a Fluid Model record and
    processing business logics.  It is an extended class of the :class:`Service`
    """

    def process(self, inputs, *args, **kwargs):
        """create Fluid record and processing business logics

        :param inputs: fields should to be updated
        :type inputs: dict
        
        :param `*args`: The variable arguments passed to this method

        :param `**kwargs`: The keyword arguments passed to this method

        :return: created fluid record
        :rtype: :class:`Fluid`
        """

        simulation = Simulation.objects.get(pk=inputs['simulation'])
        inputs['simulation'] = simulation

        # Business Logics Implementation related to the Model
        inputs = self.do_business_logics(inputs)

        # Delete key-value pair which key not in model fields
        # for example csrf token of post request
        inputs = with_keys(inputs, Fluid.fields())

        # Create Fluid record
        fluid = Fluid.objects.update_or_create(
            pk=simulation.pk,
            defaults=inputs,
        )
        
        # update simulation state
        simulation.state = Simulation.SimulationState.IPR
        simulation.save()

        return fluid

    def do_business_logics(self, inputs, *args, **kwargs):
        """processing business logics

        :param inputs: fields should to be processed
        :type inputs: dict
        
        :param `*args`: The variable arguments passed to this method

        :param `**kwargs`: The keyword arguments passed to this method

        :return: processed fields
        :rtype: dict
        """   
        
        converter = ConvertUnitService()
        
        for key in inputs:

            # unit conversion for fields which have unit
            if key+'_unit' in inputs:
                value, unit = converter.convert(key, inputs[key+'_unit'], inputs[key])
                inputs[key] = value
                inputs[key+'_unit'] = unit

            # Find Option Objcet fot Correlations fields
            if key.endswith("_option"):
                inputs[key] = Option.objects.filter(field_name=key, value=inputs[key]).first()

        return inputs


class UpdateReservoirService(Service):
    """This is a Model Service Class use for update a Reservoir Model record and
    processing business logics. It is an extended class of the :class:`Service`
    """

    def process(self, inputs, *args, **kwargs):
        """update Fluid record and processing business logics

        :param inputs: fields should to be updated
        :type inputs: dict
        
        :param `*args`: The variable arguments passed to this method

        :param `**kwargs`: The keyword arguments passed to this method

        :return: updated reservoir record
        :rtype: :class:`Reservoir`
        """
        
        reservoir = inputs['reservoir']

        # Business Logics Implementation related to the Model
        inputs = self.do_business_logics(inputs)

        # Delete key-value pair which key not in model fields
        # for example csrf token of post request
        inputs = with_keys(inputs, Reservoir.fields())

        # Update reservoir record
        reservoir = Reservoir.objects.update_or_create(
            pk=reservoir,
            defaults=inputs,
        )

        return reservoir

    def do_business_logics(self, inputs, *args, **kwargs):
        """processing business logics

        :param inputs: fields should to be processed
        :type inputs: dict
        
        :param `*args`: The variable arguments passed to this method

        :param `**kwargs`: The keyword arguments passed to this method

        :return: processed fields
        :rtype: dict
        """      
        
        converter = ConvertUnitService()
        
        for key in inputs:

            # unit conversion for fields which have unit
            if key+'_unit' in inputs:
                value, unit = converter.convert(key, inputs[key+'_unit'], inputs[key])
                inputs[key] = value
                inputs[key+'_unit'] = unit

            # Find Option Objcet fot Correlations fields
            if key.endswith("_option"):
                inputs[key] = Option.objects.filter(field_name=key, value=inputs[key]).first()

        return inputs

class CreateReservoirService(Service):
    """This is a Model Service Class use for create a Reservoir Model record and
    processing business logics.  It is an extended class of the :class:`Service`
    """

    def process(self, inputs, *args, **kwargs):
        """create Reservoir record and processing business logics

        :param inputs: fields should to be updated
        :type inputs: dict
        
        :param `*args`: The variable arguments passed to this method

        :param `**kwargs`: The keyword arguments passed to this method

        :return: created Reservoir record
        :rtype: :class:`Reservoir`
        """
        
        simulation = Simulation.objects.get(pk=inputs['simulation'])
        inputs['simulation'] = simulation

        # Business Logics Implementation related to the Model
        inputs = self.do_business_logics(inputs)

        # Delete key-value pair which key not in model fields
        # for example csrf token of post request
        temp = copy.deepcopy(inputs)
        fields = Reservoir.fields()

        for key in temp:
            if key not in fields:
                del inputs[key]

        # Create Reservoir record
        reservoir = Reservoir.objects.update_or_create(
            pk=simulation.pk,
            defaults=inputs,
        )
        
        # update simulation state
        simulation.state = Simulation.SimulationState.Well
        simulation.save()

        return reservoir

    def do_business_logics(self, inputs, *args, **kwargs):
        """processing business logics

        :param inputs: fields should to be processed
        :type inputs: dict
        
        :param `*args`: The variable arguments passed to this method

        :param `**kwargs`: The keyword arguments passed to this method

        :return: processed fields
        :rtype: dict
        """   
        
        converter = ConvertUnitService()
        
        for key in inputs:

            # unit conversion for fields which have unit
            if key+'_unit' in inputs:
                value, unit = converter.convert(key, inputs[key+'_unit'], inputs[key])
                inputs[key] = value
                inputs[key+'_unit'] = unit

            # Find Option Objcet fot Correlations fields
            if key.endswith("_option"):
                inputs[key] = Option.objects.filter(field_name=key, value=inputs[key]).first()

        return inputs


class UpdateWellService(Service):
    """This is a Model Service Class use for update a Well Model record and
    processing business logics. It is an extended class of the :class:`Service`
    """

    def process(self, inputs, *args, **kwargs):
        """update Well record and processing business logics

        :param inputs: fields should to be updated
        :type inputs: dict
        
        :param `*args`: The variable arguments passed to this method

        :param `**kwargs`: The keyword arguments passed to this method

        :return: updated Well record
        :rtype: :class:`Well`
        """
        
        well = inputs['well']

        # Business Logics Implementation related to the Model
        inputs = self.do_business_logics(inputs)

        # Delete key-value pair which key not in model fields
        # for example csrf token of post request
        inputs = with_keys(inputs, Well.fields())

        # Update Fluid record
        well = Well.objects.update_or_create(
            pk=well,
            defaults=inputs,
        )

        return well

    def do_business_logics(self, inputs, *args, **kwargs):
        """processing business logics

        :param inputs: fields should to be processed
        :type inputs: dict
        
        :param `*args`: The variable arguments passed to this method

        :param `**kwargs`: The keyword arguments passed to this method

        :return: processed fields
        :rtype: dict
        """      
        
        converter = ConvertUnitService()
        
        for key in inputs:

            # unit conversion for fields which have unit
            if key+'_unit' in inputs:
                value, unit = converter.convert(key, inputs[key+'_unit'], inputs[key])
                inputs[key] = value
                inputs[key+'_unit'] = unit

            # Find Option Objcet fot Correlations fields
            if key.endswith("_options"):
                inputs[key] = Option.objects.filter(field_name=key, value=inputs[key]).first()

        return inputs

class CreateWellService(Service):
    """This is a Model Service Class use for create a Well Model record and
    processing business logics.  It is an extended class of the :class:`Service`
    """

    def process(self, inputs, *args, **kwargs):
        """create Well record and processing business logics

        :param inputs: fields should to be updated
        :type inputs: dict
        
        :param `*args`: The variable arguments passed to this method

        :param `**kwargs`: The keyword arguments passed to this method

        :return: created Well record
        :rtype: :class:`Well`
        """
        
        simulation = Simulation.objects.get(pk=inputs['simulation'])
        inputs['simulation'] = simulation

        # Business Logics Implementation related to the Model
        inputs = self.do_business_logics(inputs)

        # Delete key-value pair which key not in model fields
        # for example csrf token of post request
        inputs = with_keys(inputs, Well.fields())

        # Create well record
        well = Well.objects.update_or_create(
            pk=simulation.pk,
            defaults=inputs,
        )
        
        # update simulation state
        simulation.state = Simulation.SimulationState.Well
        simulation.save()

        return well

    def do_business_logics(self, inputs, *args, **kwargs):
        """processing business logics

        :param inputs: fields should to be processed
        :type inputs: dict
        
        :param `*args`: The variable arguments passed to this method

        :param `**kwargs`: The keyword arguments passed to this method

        :return: processed fields
        :rtype: dict
        """   
        
        converter = ConvertUnitService()
        
        for key in inputs:

            # unit conversion for fields which have unit
            if key+'_unit' in inputs:
                value, unit = converter.convert(key, inputs[key+'_unit'], inputs[key])
                inputs[key] = value
                inputs[key+'_unit'] = unit

            # Find Option Objcet fot Correlations fields
            if key.endswith("_option"):
                inputs[key] = Option.objects.filter(field_name=key, value=inputs[key]).first()

        return inputs


class UpdatePumpService(Service):
    """This is a Model Service Class use for update a Pump Model record and
    processing business logics. It is an extended class of the :class:`Service`
    """

    def process(self, inputs, *args, **kwargs):
        """update Pump record and processing business logics

        :param inputs: fields should to be updated
        :type inputs: dict
        
        :param `*args`: The variable arguments passed to this method

        :param `**kwargs`: The keyword arguments passed to this method

        :return: updated Pump record
        :rtype: :class:`Pump`
        """
        
        pump = inputs['pump']

        # Business Logics Implementation related to the Model
        inputs = self.do_business_logics(inputs)

        # Delete key-value pair which key not in model fields
        # for example csrf token of post request
        inputs = with_keys(inputs, Pump.fields())

        # Update Pump record
        pump = Pump.objects.update_or_create(
            pk=pump,
            defaults=inputs,
        )

        return pump

    def do_business_logics(self, inputs, *args, **kwargs):
        """processing business logics

        :param inputs: fields should to be processed
        :type inputs: dict
        
        :param `*args`: The variable arguments passed to this method

        :param `**kwargs`: The keyword arguments passed to this method

        :return: processed fields
        :rtype: dict
        """      
        
        converter = ConvertUnitService()
        
        for key in inputs:

            # unit conversion for fields which have unit
            if key+'_unit' in inputs:
                value, unit = converter.convert(key, inputs[key+'_unit'], inputs[key])
                inputs[key] = value
                inputs[key+'_unit'] = unit

            # Find Option Objcet fot Correlations fields
            if key.endswith("_options"):
                inputs[key] = Option.objects.filter(field_name=key, value=inputs[key]).first()

        return inputs

class CreatePumpService(Service):
    """This is a Model Service Class use for create a Pump Model record and
    processing business logics.  It is an extended class of the :class:`Service`
    """

    def process(self, inputs, *args, **kwargs):
        """create Pump record and processing business logics

        :param inputs: fields should to be updated
        :type inputs: dict
        
        :param `*args`: The variable arguments passed to this method

        :param `**kwargs`: The keyword arguments passed to this method

        :return: created Pump record
        :rtype: :class:`Pump`
        """
        
        simulation = Simulation.objects.get(pk=inputs['simulation'])
        inputs['simulation'] = simulation

        # Business Logics Implementation related to the Model
        inputs = self.do_business_logics(inputs)

        # Delete key-value pair which key not in model fields
        # for example csrf token of post request
        inputs = with_keys(inputs, Pump.fields())

        # Create Pump record
        pump = Pump.objects.update_or_create(
            pk=simulation.pk,
            defaults=inputs,
        )
        
        # update simulation state
        simulation.state = Simulation.SimulationState.Well
        simulation.save()

        return pump

    def do_business_logics(self, inputs, *args, **kwargs):
        """processing business logics

        :param inputs: fields should to be processed
        :type inputs: dict
        
        :param `*args`: The variable arguments passed to this method

        :param `**kwargs`: The keyword arguments passed to this method

        :return: processed fields
        :rtype: dict
        """   
        
        converter = ConvertUnitService()
        
        for key in inputs:

            # unit conversion for fields which have unit
            if key+'_unit' in inputs:
                value, unit = converter.convert(key, inputs[key+'_unit'], inputs[key])
                inputs[key] = value
                inputs[key+'_unit'] = unit

            # Find Option Objcet fot Correlations fields
            if key.endswith("_option"):
                inputs[key] = Option.objects.filter(field_name=key, value=inputs[key]).first()

        return inputs


class UpdateIPRService(Service):
    """This is a Model Service Class use for update a IPR Model record and
    processing business logics. It is an extended class of the :class:`Service`
    """

    def process(self, inputs, *args, **kwargs):
        """update IPR record and processing business logics

        :param inputs: fields should to be updated
        :type inputs: dict
        
        :param `*args`: The variable arguments passed to this method

        :param `**kwargs`: The keyword arguments passed to this method

        :return: updated IPR record
        :rtype: :class:`IPR`
        """
        
        ipr = inputs['ipr']

        # Business Logics Implementation related to the Model
        inputs = self.do_business_logics(inputs)

        # Delete key-value pair which key not in model fields
        # for example csrf token of post request
        inputs = with_keys(inputs, IPR.fields())

        # Update IPR record
        ipr = IPR.objects.update_or_create(
            pk=ipr,
            defaults=inputs,
        )

        return ipr

    def do_business_logics(self, inputs, *args, **kwargs):
        """processing business logics

        :param inputs: fields should to be processed
        :type inputs: dict
        
        :param `*args`: The variable arguments passed to this method

        :param `**kwargs`: The keyword arguments passed to this method

        :return: processed fields
        :rtype: dict
        """      
        
        converter = ConvertUnitService()
        
        for key in inputs:

            # unit conversion for fields which have unit
            if key+'_unit' in inputs:
                value, unit = converter.convert(key, inputs[key+'_unit'], inputs[key])
                inputs[key] = value
                inputs[key+'_unit'] = unit

            # Find Option Objcet fot Correlations fields
            if key.endswith("_options"):
                inputs[key] = Option.objects.filter(field_name=key, value=inputs[key]).first()

        return inputs

class CreateIPRService(Service):
    """This is a Model Service Class use for create a IPR Model record and
    processing business logics.  It is an extended class of the :class:`Service`
    """

    def process(self, inputs, *args, **kwargs):
        """create IPR record and processing business logics

        :param inputs: fields should to be updated
        :type inputs: dict
        
        :param `*args`: The variable arguments passed to this method

        :param `**kwargs`: The keyword arguments passed to this method

        :return: created IPR record
        :rtype: :class:`IPR`
        """
        
        simulation = Simulation.objects.get(pk=inputs['simulation'])
        inputs['simulation'] = simulation

        # Business Logics Implementation related to the Model
        inputs = self.do_business_logics(inputs)

        # Delete key-value pair which key not in model fields
        # for example csrf token of post request
        inputs = with_keys(inputs, IPR.fields())

        # Create IPR record
        ipr = IPR.objects.update_or_create(
            pk=simulation.pk,
            defaults=inputs,
        )
        
        # update simulation state
        simulation.state = Simulation.SimulationState.Well
        simulation.save()

        return ipr

    def do_business_logics(self, inputs, *args, **kwargs):
        """processing business logics

        :param inputs: fields should to be processed
        :type inputs: dict
        
        :param `*args`: The variable arguments passed to this method

        :param `**kwargs`: The keyword arguments passed to this method

        :return: processed fields
        :rtype: dict
        """   
        
        converter = ConvertUnitService()
        
        for key in inputs:

            # unit conversion for fields which have unit
            if key+'_unit' in inputs:
                value, unit = converter.convert(key, inputs[key+'_unit'], inputs[key])
                inputs[key] = value
                inputs[key+'_unit'] = unit

            # Find Option Objcet fot Correlations fields
            if key.endswith("_option"):
                inputs[key] = Option.objects.filter(field_name=key, value=inputs[key]).first()

        return inputs


class UpdateSeparatorSizeService(Service):
    """This is a Model Service Class use for update a SeparatorSize Model record and
    processing business logics. It is an extended class of the :class:`Service`
    """

    def process(self, inputs, *args, **kwargs):
        """update SeparatorSize record and processing business logics

        :param inputs: fields should to be updated
        :type inputs: dict
        
        :param `*args`: The variable arguments passed to this method

        :param `**kwargs`: The keyword arguments passed to this method

        :return: updated SeparatorSize record
        :rtype: :class:`SeparatorSize`
        """
        
        separator_size = inputs['separator_size']

        # Business Logics Implementation related to the Model
        inputs = self.do_business_logics(inputs)

        # Delete key-value pair which key not in model fields
        # for example csrf token of post request
        inputs = with_keys(inputs, SeparatorSize.fields())

        # Update SeparatorSize record
        separator_size = SeparatorSize.objects.update_or_create(
            pk=separator_size,
            defaults=inputs,
        )

        return separator_size

    def do_business_logics(self, inputs, *args, **kwargs):
        """processing business logics

        :param inputs: fields should to be processed
        :type inputs: dict
        
        :param `*args`: The variable arguments passed to this method

        :param `**kwargs`: The keyword arguments passed to this method

        :return: processed fields
        :rtype: dict
        """      
        
        converter = ConvertUnitService()
        
        for key in inputs:

            # unit conversion for fields which have unit
            if key+'_unit' in inputs:
                value, unit = converter.convert(key, inputs[key+'_unit'], inputs[key])
                inputs[key] = value
                inputs[key+'_unit'] = unit

            # Find Option Objcet fot Correlations fields
            if key.endswith("_options"):
                inputs[key] = Option.objects.filter(field_name=key, value=inputs[key]).first()

        return inputs

class CreateSeparatorSizeService(Service):
    """This is a Model Service Class use for create a SeparatorSize Model record and
    processing business logics.  It is an extended class of the :class:`Service`
    """

    def process(self, inputs, *args, **kwargs):
        """create SeparatorSize record and processing business logics

        :param inputs: fields should to be updated
        :type inputs: dict
        
        :param `*args`: The variable arguments passed to this method

        :param `**kwargs`: The keyword arguments passed to this method

        :return: created SeparatorSize record
        :rtype: :class:`SeparatorSize`
        """
        
        simulation = Simulation.objects.get(pk=inputs['simulation'])
        inputs['simulation'] = simulation

        # Business Logics Implementation related to the Model
        inputs = self.do_business_logics(inputs)

        # Delete key-value pair which key not in model fields
        # for example csrf token of post request
        inputs = with_keys(inputs, SeparatorSize.fields())

        # Create SeparatorSize record
        separator_size = SeparatorSize.objects.update_or_create(
            pk=simulation.pk,
            defaults=inputs,
        )
        
        # update simulation state
        simulation.state = Simulation.SimulationState.Well
        simulation.save()

        return separator_size

    def do_business_logics(self, inputs, *args, **kwargs):
        """processing business logics

        :param inputs: fields should to be processed
        :type inputs: dict
        
        :param `*args`: The variable arguments passed to this method

        :param `**kwargs`: The keyword arguments passed to this method

        :return: processed fields
        :rtype: dict
        """   
        
        converter = ConvertUnitService()
        
        for key in inputs:

            # unit conversion for fields which have unit
            if key+'_unit' in inputs:
                value, unit = converter.convert(key, inputs[key+'_unit'], inputs[key])
                inputs[key] = value
                inputs[key+'_unit'] = unit

            # Find Option Objcet fot Correlations fields
            if key.endswith("_option"):
                inputs[key] = Option.objects.filter(field_name=key, value=inputs[key]).first()

        return inputs


class UpdateSeparatorService(Service):
    """This is a Model Service Class use for update a Separator Model record and
    processing business logics. It is an extended class of the :class:`Service`
    """

    def process(self, inputs, *args, **kwargs):
        """update Separator record and processing business logics

        :param inputs: fields should to be updated
        :type inputs: dict
        
        :param `*args`: The variable arguments passed to this method

        :param `**kwargs`: The keyword arguments passed to this method

        :return: updated Separator record
        :rtype: :class:`Separator`
        """
        
        separator = inputs['separator']

        # Business Logics Implementation related to the Model
        inputs = self.do_business_logics(inputs)

        # Delete key-value pair which key not in model fields
        # for example csrf token of post request
        inputs = with_keys(inputs, Separator.fields())

        # Update Separator record
        separator = Separator.objects.update_or_create(
            pk=separator,
            defaults=inputs,
        )

        return separator

    def do_business_logics(self, inputs, *args, **kwargs):
        """processing business logics

        :param inputs: fields should to be processed
        :type inputs: dict
        
        :param `*args`: The variable arguments passed to this method

        :param `**kwargs`: The keyword arguments passed to this method

        :return: processed fields
        :rtype: dict
        """      
        
        converter = ConvertUnitService()
        
        for key in inputs:

            # unit conversion for fields which have unit
            if key+'_unit' in inputs:
                value, unit = converter.convert(key, inputs[key+'_unit'], inputs[key])
                inputs[key] = value
                inputs[key+'_unit'] = unit

            # Find Option Objcet fot Correlations fields
            if key.endswith("_options"):
                inputs[key] = Option.objects.filter(field_name=key, value=inputs[key]).first()

        return inputs

class CreateSeparatorService(Service):
    """This is a Model Service Class use for create a Separator Model record and
    processing business logics.  It is an extended class of the :class:`Service`
    """

    def process(self, inputs, *args, **kwargs):
        """create Separator record and processing business logics

        :param inputs: fields should to be updated
        :type inputs: dict
        
        :param `*args`: The variable arguments passed to this method

        :param `**kwargs`: The keyword arguments passed to this method

        :return: created Separator record
        :rtype: :class:`Separator`
        """
        
        simulation = Simulation.objects.get(pk=inputs['simulation'])
        inputs['simulation'] = simulation

        # Business Logics Implementation related to the Model
        inputs = self.do_business_logics(inputs)

        # Delete key-value pair which key not in model fields
        # for example csrf token of post request
        inputs = with_keys(inputs, Separator.fields())

        # Create Separator record
        separator = Separator.objects.update_or_create(
            pk=separator.pk,
            defaults=inputs,
        )
        
        # update simulation state
        simulation.state = Simulation.SimulationState.Well
        simulation.save()

        return separator

    def do_business_logics(self, inputs, *args, **kwargs):
        """processing business logics

        :param inputs: fields should to be processed
        :type inputs: dict
        
        :param `*args`: The variable arguments passed to this method

        :param `**kwargs`: The keyword arguments passed to this method

        :return: processed fields
        :rtype: dict
        """   
        
        converter = ConvertUnitService()
        
        for key in inputs:

            # unit conversion for fields which have unit
            if key+'_unit' in inputs:
                value, unit = converter.convert(key, inputs[key+'_unit'], inputs[key])
                inputs[key] = value
                inputs[key+'_unit'] = unit

            # Find Option Objcet fot Correlations fields
            if key.endswith("_option"):
                inputs[key] = Option.objects.filter(field_name=key, value=inputs[key]).first()

        return inputs


class UpdateRodService(Service):
    """This is a Model Service Class use for update a Rod Model record and
    processing business logics. It is an extended class of the :class:`Service`
    """

    def process(self, inputs, *args, **kwargs):
        """update Rod record and processing business logics

        :param inputs: fields should to be updated
        :type inputs: dict
        
        :param `*args`: The variable arguments passed to this method

        :param `**kwargs`: The keyword arguments passed to this method

        :return: updated Rod record
        :rtype: :class:`Rod`
        """
        
        rod = inputs['rod']

        # Business Logics Implementation related to the Model
        inputs = self.do_business_logics(inputs)

        # Delete key-value pair which key not in model fields
        # for example csrf token of post request
        inputs = with_keys(inputs, Rod.fields())

        # Update Rod record
        rod = Rod.objects.update_or_create(
            pk=rod,
            defaults=inputs,
        )

        return rod

    def do_business_logics(self, inputs, *args, **kwargs):
        """processing business logics

        :param inputs: fields should to be processed
        :type inputs: dict
        
        :param `*args`: The variable arguments passed to this method

        :param `**kwargs`: The keyword arguments passed to this method

        :return: processed fields
        :rtype: dict
        """      
        
        converter = ConvertUnitService()
        
        for key in inputs:

            # unit conversion for fields which have unit
            if key+'_unit' in inputs:
                value, unit = converter.convert(key, inputs[key+'_unit'], inputs[key])
                inputs[key] = value
                inputs[key+'_unit'] = unit

            # Find Option Objcet fot Correlations fields
            if key.endswith("_options"):
                inputs[key] = Option.objects.filter(field_name=key, value=inputs[key]).first()

        return inputs

class CreateRodService(Service):
    """This is a Model Service Class use for create a Rod Model record and
    processing business logics.  It is an extended class of the :class:`Service`
    """

    def process(self, inputs, *args, **kwargs):
        """create Rod record and processing business logics

        :param inputs: fields should to be updated
        :type inputs: dict
        
        :param `*args`: The variable arguments passed to this method

        :param `**kwargs`: The keyword arguments passed to this method

        :return: created Rod record
        :rtype: :class:`Rod`
        """
        
        simulation = Simulation.objects.get(pk=inputs['simulation'])
        inputs['simulation'] = simulation

        # Business Logics Implementation related to the Model
        inputs = self.do_business_logics(inputs)

        # Delete key-value pair which key not in model fields
        # for example csrf token of post request
        inputs = with_keys(inputs, Rod.fields())

        # Create Rod record
        rod = Rod.objects.update_or_create(
            pk=simulation.pk,
            defaults=inputs,
        )
        
        # update simulation state
        simulation.state = Simulation.SimulationState.Well
        simulation.save()

        return rod

    def do_business_logics(self, inputs, *args, **kwargs):
        """processing business logics

        :param inputs: fields should to be processed
        :type inputs: dict
        
        :param `*args`: The variable arguments passed to this method

        :param `**kwargs`: The keyword arguments passed to this method

        :return: processed fields
        :rtype: dict
        """   
        
        converter = ConvertUnitService()
        
        for key in inputs:

            # unit conversion for fields which have unit
            if key+'_unit' in inputs:
                value, unit = converter.convert(key, inputs[key+'_unit'], inputs[key])
                inputs[key] = value
                inputs[key+'_unit'] = unit

            # Find Option Objcet fot Correlations fields
            if key.endswith("_option"):
                inputs[key] = Option.objects.filter(field_name=key, value=inputs[key]).first()

        return inputs


class UpdatePumpUnitService(Service):
    """This is a Model Service Class use for update a PumpUnit Model record and
    processing business logics. It is an extended class of the :class:`Service`
    """

    def process(self, inputs, *args, **kwargs):
        """update PumpUnit record and processing business logics

        :param inputs: fields should to be updated
        :type inputs: dict
        
        :param `*args`: The variable arguments passed to this method

        :param `**kwargs`: The keyword arguments passed to this method

        :return: updated PumpUnit record
        :rtype: :class:`PumpUnit`
        """
        
        pump_unit = inputs['pump_unit']

        # Business Logics Implementation related to the Model
        inputs = self.do_business_logics(inputs)

        # Delete key-value pair which key not in model fields
        # for example csrf token of post request
        inputs = with_keys(inputs, PumpUnit.fields())

        # Update PumpUnit record
        pump_unit = PumpUnit.objects.update_or_create(
            pk=pump_unit,
            defaults=inputs,
        )

        return pump_unit

    def do_business_logics(self, inputs, *args, **kwargs):
        """processing business logics

        :param inputs: fields should to be processed
        :type inputs: dict
        
        :param `*args`: The variable arguments passed to this method

        :param `**kwargs`: The keyword arguments passed to this method

        :return: processed fields
        :rtype: dict
        """      
        
        converter = ConvertUnitService()
        
        for key in inputs:

            # unit conversion for fields which have unit
            if key+'_unit' in inputs:
                value, unit = converter.convert(key, inputs[key+'_unit'], inputs[key])
                inputs[key] = value
                inputs[key+'_unit'] = unit

            # Find Option Objcet fot Correlations fields
            if key.endswith("_options"):
                inputs[key] = Option.objects.filter(field_name=key, value=inputs[key]).first()

        return inputs

class CreatePumpUnitService(Service):
    """This is a Model Service Class use for create a PumpUnit Model record and
    processing business logics.  It is an extended class of the :class:`Service`
    """

    def process(self, inputs, *args, **kwargs):
        """create PumpUnit record and processing business logics

        :param inputs: fields should to be updated
        :type inputs: dict
        
        :param `*args`: The variable arguments passed to this method

        :param `**kwargs`: The keyword arguments passed to this method

        :return: created PumpUnit record
        :rtype: :class:`PumpUnit`
        """
        
        simulation = Simulation.objects.get(pk=inputs['simulation'])
        inputs['simulation'] = simulation

        # Business Logics Implementation related to the Model
        inputs = self.do_business_logics(inputs)

        # Delete key-value pair which key not in model fields
        # for example csrf token of post request
        inputs = with_keys(inputs, PumpUnit.fields())

        # Create Rod record
        pump_unit = PumpUnit.objects.update_or_create(
            pk=simulation.pk,
            defaults=inputs,
        )
        
        # update simulation state
        simulation.state = Simulation.SimulationState.Well
        simulation.save()

        return pump_unit

    def do_business_logics(self, inputs, *args, **kwargs):
        """processing business logics

        :param inputs: fields should to be processed
        :type inputs: dict
        
        :param `*args`: The variable arguments passed to this method

        :param `**kwargs`: The keyword arguments passed to this method

        :return: processed fields
        :rtype: dict
        """   
        
        converter = ConvertUnitService()
        
        for key in inputs:

            # unit conversion for fields which have unit
            if key+'_unit' in inputs:
                value, unit = converter.convert(key, inputs[key+'_unit'], inputs[key])
                inputs[key] = value
                inputs[key+'_unit'] = unit

            # Find Option Objcet fot Correlations fields
            if key.endswith("_option"):
                inputs[key] = Option.objects.filter(field_name=key, value=inputs[key]).first()

        return inputs


class UpdateGearboxService(Service):
    """This is a Model Service Class use for update a Gearbox Model record and
    processing business logics. It is an extended class of the :class:`Service`
    """

    def process(self, inputs, *args, **kwargs):
        """update Gearbox record and processing business logics

        :param inputs: fields should to be updated
        :type inputs: dict
        
        :param `*args`: The variable arguments passed to this method

        :param `**kwargs`: The keyword arguments passed to this method

        :return: updated Gearbox record
        :rtype: :class:`Gearbox`
        """
        
        gearbox = inputs['gearbox']

        # Business Logics Implementation related to the Model
        inputs = self.do_business_logics(inputs)

        # Delete key-value pair which key not in model fields
        # for example csrf token of post request
        inputs = with_keys(inputs, Gearbox.fields())

        # Update Gearbox record
        gearbox = Gearbox.objects.update_or_create(
            pk=gearbox,
            defaults=inputs,
        )

        return gearbox

    def do_business_logics(self, inputs, *args, **kwargs):
        """processing business logics

        :param inputs: fields should to be processed
        :type inputs: dict
        
        :param `*args`: The variable arguments passed to this method

        :param `**kwargs`: The keyword arguments passed to this method

        :return: processed fields
        :rtype: dict
        """      
        
        converter = ConvertUnitService()
        
        for key in inputs:

            # unit conversion for fields which have unit
            if key+'_unit' in inputs:
                value, unit = converter.convert(key, inputs[key+'_unit'], inputs[key])
                inputs[key] = value
                inputs[key+'_unit'] = unit

            # Find Option Objcet fot Correlations fields
            if key.endswith("_options"):
                inputs[key] = Option.objects.filter(field_name=key, value=inputs[key]).first()

        return inputs

class CreateGearboxService(Service):
    """This is a Model Service Class use for create a Gearbox Model record and
    processing business logics.  It is an extended class of the :class:`Service`
    """

    def process(self, inputs, *args, **kwargs):
        """create Gearbox record and processing business logics

        :param inputs: fields should to be updated
        :type inputs: dict
        
        :param `*args`: The variable arguments passed to this method

        :param `**kwargs`: The keyword arguments passed to this method

        :return: created Gearbox record
        :rtype: :class:`Gearbox`
        """
        
        simulation = Simulation.objects.get(pk=inputs['simulation'])
        inputs['simulation'] = simulation

        # Business Logics Implementation related to the Model
        inputs = self.do_business_logics(inputs)

        # Delete key-value pair which key not in model fields
        # for example csrf token of post request
        inputs = with_keys(inputs, Gearbox.fields())

        # Create Gearbox record
        gearbox = Gearbox.objects.update_or_create(
            pk=simulation.pk,
            defaults=inputs,
        )
        
        # update simulation state
        simulation.state = Simulation.SimulationState.Well
        simulation.save()

        return gearbox

    def do_business_logics(self, inputs, *args, **kwargs):
        """processing business logics

        :param inputs: fields should to be processed
        :type inputs: dict
        
        :param `*args`: The variable arguments passed to this method

        :param `**kwargs`: The keyword arguments passed to this method

        :return: processed fields
        :rtype: dict
        """   
        
        converter = ConvertUnitService()
        
        for key in inputs:

            # unit conversion for fields which have unit
            if key+'_unit' in inputs:
                value, unit = converter.convert(key, inputs[key+'_unit'], inputs[key])
                inputs[key] = value
                inputs[key+'_unit'] = unit

            # Find Option Objcet fot Correlations fields
            if key.endswith("_option"):
                inputs[key] = Option.objects.filter(field_name=key, value=inputs[key]).first()

        return inputs


class UpdateMotorService(Service):
    """This is a Model Service Class use for update a Motor Model record and
    processing business logics. It is an extended class of the :class:`Service`
    """

    def process(self, inputs, *args, **kwargs):
        """update Motor record and processing business logics

        :param inputs: fields should to be updated
        :type inputs: dict
        
        :param `*args`: The variable arguments passed to this method

        :param `**kwargs`: The keyword arguments passed to this method

        :return: updated Motor record
        :rtype: :class:`Motor`
        """
        
        motor = inputs['motor']

        # Business Logics Implementation related to the Model
        inputs = self.do_business_logics(inputs)

        # Delete key-value pair which key not in model fields
        # for example csrf token of post request
        inputs = with_keys(inputs, Motor.fields())

        # Update Motor record
        motor = Motor.objects.update_or_create(
            pk=motor,
            defaults=inputs,
        )

        return motor

    def do_business_logics(self, inputs, *args, **kwargs):
        """processing business logics

        :param inputs: fields should to be processed
        :type inputs: dict
        
        :param `*args`: The variable arguments passed to this method

        :param `**kwargs`: The keyword arguments passed to this method

        :return: processed fields
        :rtype: dict
        """      
        
        converter = ConvertUnitService()
        
        for key in inputs:

            # unit conversion for fields which have unit
            if key+'_unit' in inputs:
                value, unit = converter.convert(key, inputs[key+'_unit'], inputs[key])
                inputs[key] = value
                inputs[key+'_unit'] = unit

            # Find Option Objcet fot Correlations fields
            if key.endswith("_options"):
                inputs[key] = Option.objects.filter(field_name=key, value=inputs[key]).first()

        return inputs

class CreateMotorService(Service):
    """This is a Model Service Class use for create a Motor Model record and
    processing business logics.  It is an extended class of the :class:`Service`
    """

    def process(self, inputs, *args, **kwargs):
        """create Motor record and processing business logics

        :param inputs: fields should to be updated
        :type inputs: dict
        
        :param `*args`: The variable arguments passed to this method

        :param `**kwargs`: The keyword arguments passed to this method

        :return: created Motor record
        :rtype: :class:`Motor`
        """
        
        simulation = Simulation.objects.get(pk=inputs['simulation'])
        inputs['simulation'] = simulation

        # Business Logics Implementation related to the Model
        inputs = self.do_business_logics(inputs)

        # Delete key-value pair which key not in model fields
        # for example csrf token of post request
        inputs = with_keys(inputs, Motor.fields())

        # Create Motor record
        motor = Motor.objects.update_or_create(
            pk=simulation.pk,
            defaults=inputs,
        )
        
        # update simulation state
        simulation.state = Simulation.SimulationState.Well
        simulation.save()

        return motor

    def do_business_logics(self, inputs, *args, **kwargs):
        """processing business logics

        :param inputs: fields should to be processed
        :type inputs: dict
        
        :param `*args`: The variable arguments passed to this method

        :param `**kwargs`: The keyword arguments passed to this method

        :return: processed fields
        :rtype: dict
        """   
        
        converter = ConvertUnitService()
        
        for key in inputs:

            # unit conversion for fields which have unit
            if key+'_unit' in inputs:
                value, unit = converter.convert(key, inputs[key+'_unit'], inputs[key])
                inputs[key] = value
                inputs[key+'_unit'] = unit

            # Find Option Objcet fot Correlations fields
            if key.endswith("_option"):
                inputs[key] = Option.objects.filter(field_name=key, value=inputs[key]).first()

        return inputs

