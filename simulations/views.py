from utils.Exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from simulations.models import OdWeightId, Option, Simulation, Membership, Role, Fluid, IPR, Well, Separator, SeparatorSize, Rod, PumpUnit, Reservoir
from srp.decorators import user_is_simulation_owner, user_has_access_to_simulation, valid_simulation

from .forms import FluidPanelForm, ReservoirPanelForm, GearBoxFormPanel, MotorPanelForm, WellPanelForm, SeparatorPanelForm, PumpPanelForm, RodPanelForm, PumpUnitFormPanel
from .services import DummyModuleService, UpdateFluidService, CreateFluidService, UpdateSeparatorService, CreateSeparatorService, UpdateReservoirService, CreateReservoirService
from .filters import FluidFilter
from utils.general_utils import with_keys, without_keys
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from itertools import zip_longest
from django.http import JsonResponse



def simulations(request):
    """if the user is logged in redirects to simulations index, otherwise redirects the user to the login page

    Args:
        request (GET): None

    Returns:
        HttpResponse: redirection to simulations or login
    """
    # check if user is logged in, redirect to login page if not
    if (not request.user.is_authenticated):
        return redirect('users:signin')
        # return HttpResponse('redirect to login')

    owner = Role.objects.filter(name='owner').first()
    simulations = request.user.simulations.all()
    if owner:
        for simulation in simulations:
            membership = simulation.membership_set.all().filter(role=owner).first()
            if membership:
                simulation.creator = membership.user

    return render(request, 'simulations/index.html', {'simulations': simulations})


def create(request):
    """if the user is logged in redirects to simulations index, otherwise redirects the user to the login page

    Args:
        request (GET): None

    Returns:
        HttpResponse: redirection to simulations or login
    """
    # check if user is logged in, redirect to login page if not
    if (not request.user.is_authenticated):
        return redirect('users:signin')
    # if its a GET request show the create form
    if (request.method == 'GET'):
        return render(request, 'simulations/create.html')
    # if its a POST request test the credential
    elif (request.method == 'POST'):
        simulation = Simulation.objects.filter(url=request.POST.get('url').lower())
        if simulation:
            messages.error(request, "this url has used before")
            return redirect('users:dashboard')

        name = request.POST.get('name')
        url = request.POST.get('url').lower()
        description = request.POST.get('description')
        visibility = request.POST.get('visibility')
        simulation = Simulation(name=name, url=url, description=description, visibility=visibility,
                                state=Simulation.SimulationState.Fluid)
        simulation.save()

        membership = Membership(user=request.user, role=Role.objects.filter(name='owner').first(),
                                simulation=simulation)
        membership.save()
        return redirect('simulations:run', url)


def update(request):
    """if the user is logged in redirects to simulations index, otherwise redirects the user to the login page

    Args:
        request (GET): None

    Returns:
        HttpResponse: redirection to simulations or login
    """
    # check if user is logged in, redirect to login page if not
    if (not request.user.is_authenticated):
        return redirect('users:signin')
    # if its a GET request show the create form
    # if(request.method == 'GET'):
    #     return render(request, 'simulations/create.html')
    # if its a POST request test the credential
    elif (request.method == 'POST'):
        simulations = Simulation.objects.filter(url=request.POST.get('url').lower())
        if not simulations:
            messages.error(request, "simulation not found")
            return redirect('users:dashboard')

        simulation = simulations[0]

        if request.POST.get('name'):
            simulation.name = request.POST.get('name')
        if request.POST.get('url'):
            simulation.url = request.POST.get('url').lower()
        if request.POST.get('description'):
            simulation.name = request.POST.get('description')
        if request.POST.get('visibility'):
            simulation.url = request.POST.get('visibility')

        simulation.save()

        return redirect('simulations:simulations')


@user_is_simulation_owner
def delete(request, simulation_url):
    """if the user is logged in redirects to simulations index, otherwise redirects the user to the login page

    Args:
        request (GET): None

    Returns:
        HttpResponse: redirection to simulations or login
    """
    # check if user is logged in, redirect to login page if not
    if (not request.user.is_authenticated):
        return redirect('users:signin')
    # if its a GET request show the create form
    # if(request.method == 'GET'):
    #     return render(request, 'simulations/create.html')
    # if its a POST request test the credential
    elif (request.method == 'POST'):
        simulations = Simulation.objects.filter(url=simulation_url)
        if not simulations:
            messages.error(request, "simulation not found")
            return redirect('simulations:simulations')

        simulation = simulations[0]

        simulation.delete()

        return redirect('simulations:simulations')


def run(request, simulation_url):
    """if the user is logged in redirects to simulations run, otherwise redirects the user to the login page

    Args:
        request (GET): None

    Returns:
        HttpResponse: redirection to simulations.run or login
    """
    # check if user is logged in, redirect to login page if not
    if (not request.user.is_authenticated):
        return redirect('main:signin')
    # if its a GET request show the create form
    if (request.method == 'GET'):

        simulation = Simulation.objects.filter(url=simulation_url).first()
        if not simulation:
            messages.error(request, "simulation not found")
            return redirect('users:dashboard')

        owner = Role.objects.filter(name='owner').first()
        membership = simulation.membership_set.all().filter(role=owner).first()
        if membership:
            simulation.creator = membership.user

        if simulation.state == Simulation.SimulationState.Fluid:
            return redirect('/simulations/run/' + simulation.url + '/fluid', {'simulation': simulation})
        elif simulation.state == Simulation.SimulationState.IPR:
            return redirect('/simulations/run/' + simulation.url + '/reservoir', {'simulation': simulation})
        elif simulation.state == Simulation.SimulationState.Well:
            return redirect('/simulations/run/' + simulation.url + '/well', {'simulation': simulation})
        elif simulation.state == Simulation.SimulationState.Separator:
            return redirect('/simulations/run/' + simulation.url + '/separator', {'simulation': simulation})
        elif simulation.state == Simulation.SimulationState.Rod:
            return redirect('/simulations/run/' + simulation.url + '/rod', {'simulation': simulation})
        elif simulation.state == Simulation.SimulationState.PumpUnit:
            return redirect('/simulations/run/' + simulation.url + '/pump_unit', {'simulation': simulation})
        elif simulation.state == Simulation.SimulationState.SurfaceEquipment:
            return redirect('/simulations/run/' + simulation.url + '/surface_equipment', {'simulation': simulation})
        else:
            owner = Role.objects.filter(name='owner').first()
            simulations = request.user.simulations.all()
            if owner:
                for simulation in simulations:
                    membership = simulation.membership_set.all().filter(role=owner).first()
                    if membership:
                        simulation.creator = membership.user

            return redirect('/simulations')
    # if its a POST request test the credential
    # elif(request.method == 'POST'):
    #     name = request.POST.get('name')
    #     description = request.POST.get('description')
    #     visibility = request.POST.get('visibility')
    #     simulation = Simulation(name=name, description=description, visibility=visibility, state = 1)
    #     simulation.save()

    #     return render(request, 'simulations/run.html')

@login_required
@user_has_access_to_simulation
def run_fluid(request, simulation_url):
    """redirects to simulations run_fluid

    Args:
        request (GET): None
        request (POST): None
        simulation_url (str): url of requested simulation

    Returns:
        HttpResponse: redirection to simulations:run.fluid
    """

    simulation = Simulation.objects.filter(url=simulation_url).first()

    # if there is no such simulation as requested, redirect to simulations index
    if not simulation:
        messages.error(request, "simulation not found")
        return redirect('simulations:simulations')


    # if it's a GET request show the input form
    if (request.method == 'GET'):

        if simulation.has_fluid() and simulation.has_separator():
            form = FluidPanelForm(
                initial={
                    # General Fields
                    'bubble_point_pressure': simulation.fluid.bubble_point_pressure,
                    'flow_rate_at_test_buttom_hole_pressure': simulation.fluid.flow_rate_at_test_buttom_hole_pressure,
                    'gas_composition': simulation.fluid.gas_composition,
                    'gas_oil_ratio': simulation.fluid.gas_oil_ratio,
                    'gas_specific_gravity': simulation.fluid.gas_specific_gravity,
                    'gas_viscosity': simulation.fluid.gas_viscosity,
                    'oil_composition': simulation.fluid.oil_composition,
                    'oil_gravity': simulation.fluid.oil_gravity,
                    'oil_specific_gravity': simulation.fluid.oil_specific_gravity,
                    'oil_viscosity': simulation.fluid.oil_viscosity,
                    'saturate_pressure': simulation.fluid.saturate_pressure,
                    'static_buttom_hole_pressure': simulation.fluid.static_buttom_hole_pressure,
                    'test_buttom_hole_pressure': simulation.fluid.test_buttom_hole_pressure,
                    'total_flow_rate': simulation.fluid.total_flow_rate,
                    'water_cut': simulation.fluid.water_cut,
                    'water_salinity': simulation.fluid.water_salinity,
                    'water_specific_gravity': simulation.fluid.water_specific_gravity,
                    # Gas Impurities
                    'co2': simulation.fluid.co2,
                    'h2s': simulation.fluid.h2s,
                    'n2': simulation.fluid.n2,
                    # Correlations
                    'bubble_point_pressure_correlation_option': simulation.fluid.bubble_point_pressure_correlation_option.value,
                    'oil_gravity_correlation_option': simulation.fluid.oil_gravity_correlation_option.value,
                    'gas_impurities_correlation_option': simulation.fluid.gas_impurities_correlation_option.value,
                    'gas_oil_ratio_correlation_option': simulation.fluid.gas_oil_ratio_correlation_option.value,
                    'gas_specific_gravity_correlation_option': simulation.fluid.gas_specific_gravity_correlation_option.value,
                    'water_cut_correlation_option': simulation.fluid.water_cut_correlation_option.value,
                    'water_specific_gravity_correlation_option': simulation.fluid.water_specific_gravity_correlation_option.value,
                    ### Separator Model
                    'depth_of_separator_installation': simulation.separator.depth_of_separator_installation,
                    # Separator Related
                    'gas_density': simulation.fluid.gas_density,
                    'oil_api': simulation.fluid.oil_api,
                    'water_density': simulation.fluid.water_density,
                    'water_viscosity': simulation.fluid.water_viscosity,
                    # Pump Related
                    "gor_at_pump_inlet": simulation.fluid.gor_at_pump_inlet,
                    "oil_bubble_point_pressure_at_inlet": simulation.fluid.oil_bubble_point_pressure_at_inlet,
                    "oil_density_at_pump_inlet": simulation.fluid.oil_density_at_pump_inlet,
                    "oil_pressure_at_pump_inlet": simulation.fluid.oil_pressure_at_pump_inlet,
                    "oil_temperature_at_pump_inlet": simulation.fluid.oil_temperature_at_pump_inlet,
                    "wellhead_pressure": simulation.fluid.wellhead_pressure,
                }
            )
        else:
            form = FluidPanelForm(None)

        # get simulation owner and add it to simulation instance
        owner = Role.objects.filter(name='owner').first()
        membership = simulation.membership_set.all().filter(role=owner).first()
        if membership:
            simulation.creator = membership.user

        # twisted_form = zip_longest(*[iter(form)] * 2)

        return render(request, 'simulations/fluid.html', {'simulation': simulation, "form": form})

    # if it's a POST request save data and show ipr form
    if (request.method == 'POST'):

        form = FluidPanelForm(request.POST)

        # check whether form is valid
        if form.is_valid():
            
            fluid_fields = dict(request.POST.items())
            # if requested simulation has fluid record, update that record
            if simulation.has_fluid():
                # add primary key of record which used in updating process
                fluid_fields['fluid'] = simulation.fluid.pk

                # pass validated input data to service,
                # in order to processing business logic and update record
                fluid = UpdateFluidService.execute(fluid_fields)

            # otherwise, create a new fluid record
            else:
                # add primary key of related simulation record which used in creating process
                fluid_fields['simulation'] = simulation.pk

                # pass validated input data to service,
                # in order to processing business logic and update record
                fluid = CreateFluidService.execute(fluid_fields)

            separator_fields = dict(request.POST.items())
            # if requested simulation has fluid record, update that record
            if simulation.has_separator():
                separator_fields = with_keys(
                                        dict(request.POST.items()), 
                                        ['depth_of_separator_installation',
                                        'depth_of_separator_installation_unit',]
                                    )

                # add primary key of record which used in updating process
                separator_fields['separator'] = simulation.separator.pk

                # pass validated input data to service,
                # in order to processing business logic and update record
                separator = UpdateSeparatorService.execute(separator_fields)

            # otherwise, create a new fluid record
            else:
                # add primary key of related simulation record which used in creating process
                separator_fields['simulation'] = simulation.pk

                # pass validated input data to service,
                # in order to processing business logic and update record
                separator = CreateSeparatorService.execute(separator_fields)

            return redirect('/simulations/run/' + simulation.url + '/reservoir', {'simulation': simulation})

        return render(request, 'simulations/fluid.html', {'simulation': simulation, "form": form})


class RunReservoir(View):
    
    @method_decorator(login_required)
    @method_decorator(valid_simulation)
    @method_decorator(user_has_access_to_simulation)
    def get(self, request, simulation_url):

        simulation = Simulation.objects.filter(url=simulation_url).first()

        if simulation.has_reservoir():
            form = ReservoirPanelForm(
                initial={
                    # General Fields
                    'reservoir_temperature': simulation.reservoir.reservoir_temperature,
                    'reservoir_pressure': simulation.reservoir.reservoir_pressure,
                    'flow_rate_vs_pressure': simulation.reservoir.flow_rate_vs_pressure,
                    'reservoir_type_option': simulation.reservoir.reservoir_type_option.value,
                }
            )
        else:
            form = ReservoirPanelForm(None)

        # get simulation owner and add it to simulation instance
        owner = Role.objects.filter(name='owner').first()
        membership = simulation.membership_set.all().filter(role=owner).first()
        if membership:
            simulation.creator = membership.user

        return render(request, 'simulations/reservoir.html', {'simulation': simulation, "form": form})


    @method_decorator(login_required)
    @method_decorator(valid_simulation)
    @method_decorator(user_has_access_to_simulation)
    def post(self, request, simulation_url):

        form = ReservoirPanelForm(request.POST)

        simulation = Simulation.objects.filter(url=simulation_url).first()

        # check whether form is valid
        if form.is_valid():
            
            reservoir_fields = dict(request.POST.items())
            # if requested simulation has fluid record, update that record
            if simulation.has_reservoir():
                # add primary key of record which used in updating process
                reservoir_fields['reservoir'] = simulation.reservoir.pk

                # pass validated input data to service,
                # in order to processing business logic and update record
                reservoir = UpdateReservoirService.execute(reservoir_fields)

            # otherwise, create a new fluid record
            else:
                # add primary key of related simulation record which used in creating process
                reservoir_fields['simulation'] = simulation.pk

                # pass validated input data to service,
                # in order to processing business logic and update record
                reservoir = CreateReservoirService.execute(reservoir_fields)

            return redirect('/simulations/run/' + simulation.url + '/well', {'simulation': simulation})
        else:
            return redirect('/simulations/run/' + simulation.url + '/reservoir', {'simulation': simulation, 'form': form})



class RunSeparator(View):
    def get(self, request, simulation_url):

        simulation = Simulation.objects.filter(url=simulation_url).first()

        if simulation and simulation.has_separator():
            form = SeparatorPanelForm(
                initial={
                    "length": simulation.separator.length,
                    "input_pressure_drop": simulation.separator.input_pressure_drop,
                    "input_efficiency": simulation.separator.input_efficiency,
                }
            )
        else:
            form = SeparatorPanelForm(None)

        if not simulation:
            messages.error(request, "simulation not found")
            return redirect('simulations:simulations')

        owner = Role.objects.filter(name='owner').first()
        membership = simulation.membership_set.all().filter(role=owner).first()
        if membership:
            simulation.creator = membership.user

        return render(request, 'simulations/separator.html', {'simulation': simulation, "form": form})

        # if there is no such simulation as requested, redirect to simulations index

    def post(self, request, simulation_url):
        simulation = Simulation.objects.filter(url=simulation_url).first()

        # if there is no such simulation as requested, redirect to simulations index
        if not simulation:
            messages.error(request, "simulation not found")
            return redirect('simulations:simulations')

        form = SeparatorPanelForm(request.POST)
        if form.is_valid():
            # if requested simulation has fluid record, update that record
            if simulation.has_separator():
                inputs = dict(request.POST.items())
                inputs['simulation'] = simulation.separator.pk

                # pass validated input data to service,
                # in order to processing business logic and update record
                # separator = UpdateSeparatorService.execute(inputs)

            # otherwise, create a new fluid record
            else:
                inputs = dict(request.POST.items())
                inputs['simulation'] = simulation.pk

                # pass validated input data to service,
                # in order to processing business logic and update record
                # separator = CreateSeparatorService.execute(inputs)


        return render(request, 'simulations/separator.html', { 'simulation' : simulation, "form": form })
        # return redirect('/simulations/run/' + simulation.url + '/separator', {'simulation': simulation})


class RunPumpUnit(View):
    def get(self, request, simulation_url):
        simulation = Simulation.objects.filter(url=simulation_url).first()

        if (not request.user.is_authenticated):
            return redirect('users:signin')

        if simulation and simulation.has_pumpunit():
            form = PumpUnitFormPanel(
                initial={
                    "Kinematics_for_Polished_rods": simulation.pumpunit.Kinematics_for_Polished_rods,
                }
            )
        else:
            form = PumpUnitFormPanel(None)

        if not simulation:
            owner = Role.objects.filter(name='owner').first()
            simulations = request.user.simulations.all()
            if owner:
                for simulation in simulations:
                    membership = simulation.membership_set.all().filter(role=owner).first()
                    if membership:
                        simulation.creator = membership.user

            messages.error(request, "simulation not found")
            return redirect('simulations:simulations')

        owner = Role.objects.filter(name='owner').first()
        membership = simulation.membership_set.all().filter(role=owner).first()
        if membership:
            simulation.creator = membership.user

        return render(request, 'simulations/pump_unit.html', {'simulation': simulation, "form": form})

    def post(self, request, simulation_url):

        if (not request.user.is_authenticated):
            return redirect('users:signin')

        form = PumpUnitFormPanel(request.POST)

        simulation = Simulation.objects.filter(url=simulation_url).first()

        if form.is_valid():
            if simulation.has_pumpunit():
                inputs = dict(request.POST.items())
                inputs['simulation'] = simulation.separator.pk
                return redirect('/simulations/run/' + simulation.url + '/surface_equipment', {'simulation': simulation})

                # pumpunit = UpdatePumpUnitService.execute(inputs)
        else:
            inputs = dict(request.POST.items())
            inputs['simulation'] = simulation.pk
            return render(request, 'simulations/pump_unit.html', {'simulation': simulation, "form": form})


        return redirect('/simulations/run/' + simulation.url + '/surface_equipment', {'simulation': simulation})


class RunRod(View):
    def get(self, request, simulation_url):
        simulation = Simulation.objects.filter(url=simulation_url).first()
        if not simulation:
            owner = Role.objects.filter(name='owner').first()
            simulations = request.user.simulations.all()
            if owner:
                for simulation in simulations:
                    membership = simulation.membership_set.all().filter(role=owner).first()
                    if membership:
                        simulation.creator = membership.user

            messages.error(request, "simulation not found")
            return redirect('simulations:simulations')

        if simulation and simulation.has_rod():
            form = RodPanelForm(
                initial={
                    "rods_dia": simulation.rod.rods_dia,
                    "elasticity": simulation.rod.elasticity,
                    "polished_rod_friction_force": simulation.rod.polished_rod_friction_force,
                    "string_length": simulation.rod.string_length,
                    "weight_per_unit_Length": simulation.rod.weight_per_unit_Length,
                }
            )
        else:
            form = RodPanelForm(None)

        owner = Role.objects.filter(name='owner').first()
        membership = simulation.membership_set.all().filter(role=owner).first()
        if membership:
            simulation.creator = membership.user

        return render(request, 'simulations/rod.html', {'simulation': simulation, "form": form})

    def post(self, request, simulation_url):
        if (not request.user.is_authenticated):
            return redirect('users:signin')

        form = RodPanelForm(request.POST)

        simulation = Simulation.objects.filter(url=simulation_url).first()

        if form.is_valid():
            if simulation.has_rod():
                inputs = dict(request.POST.items())
                inputs['simulation'] = simulation.separator.pk
                return redirect('/simulations/run/' + simulation.url + '/rod', {'simulation': simulation})

                # rod = UpdateRodService.execute(inputs)
        else:
            inputs = dict(request.POST.items())
            inputs['simulation'] = simulation.pk
            return render(request, 'simulations/rod.html', {'simulation': simulation, "form": form})


class RunPump(View):
    def get(self, request, simulation_url):
        simulation = Simulation.objects.filter(url=simulation_url).first()
        if not simulation:
            owner = Role.objects.filter(name='owner').first()
            simulations = request.user.simulations.all()
            if owner:
                for simulation in simulations:
                    membership = simulation.membership_set.all().filter(role=owner).first()
                    if membership:
                        simulation.creator = membership.user

            messages.error(request, "simulation not found")
            return redirect('simulations:simulations')

        if simulation and simulation.has_pumpunit():
            form = PumpPanelForm(
                initial={
                    "pump_depth": simulation.pump.pump_depth,
                }
            )
        else:
          form = PumpPanelForm(None)

        owner = Role.objects.filter(name='owner').first()
        membership = simulation.membership_set.all().filter(role=owner).first()
        if membership:
            simulation.creator = membership.user

        return render(request, 'simulations/pump.html', {'simulation': simulation, "form": form})

    def post(self, request, simulation_url):
        simulation = Simulation.objects.filter(url=simulation_url).first()

        # if there is no such simulation as requested, redirect to simulations index
        if not simulation:
            messages.error(request, "simulation not found")
            return redirect('simulations:simulations')

        form = PumpPanelForm(request.POST)
        if form.is_valid():
            # if requested simulation has fluid record, update that record
            if simulation.has_separator():
                inputs = dict(request.POST.items())
                inputs['simulation'] = simulation.separator.pk

                # pass validated input data to service,
                # in order to processing business logic and update record
                # separator = UpdateSeparatorService.execute(inputs)

            # otherwise, create a new fluid record
            else:
                inputs = dict(request.POST.items())
                inputs['simulation'] = simulation.pk

                # pass validated input data to service,
                # in order to processing business logic and update record
                # pump = UpdatePumpService.execute(inputs)

        return render(request, 'simulations/pump.html', {'simulation': simulation, "form": form})


class RunWell(View):
    def get(self, request, simulation_url):
        if (not request.user.is_authenticated):
            return redirect('users:signin')

        simulation = Simulation.objects.filter(url=simulation_url).first()
        if not simulation:
            owner = Role.objects.filter(name='owner').first()
            simulations = request.user.simulations.all()
            if owner:
                for simulation in simulations:
                    membership = simulation.membership_set.all().filter(role=owner).first()
                    if membership:
                        simulation.creator = membership.user

            messages.error(request, "simulation not found")
            return redirect('simulations:simulations')

        if simulation and simulation.has_well():
            form = WellPanelForm(
                initial={}
            )
        else:
            form = WellPanelForm(None)

        owner = Role.objects.filter(name='owner').first()
        membership = simulation.membership_set.all().filter(role=owner).first()
        if membership:
            simulation.creator = membership.user

        return render(request, 'simulations/well.html', {'simulation': simulation, "form": form})


    def post(self, request, simulation_url):
        pass


def run_well(request, simulation_url):
    """if the user is logged in redirects to simulations run, otherwise redirects the user to the login page

    Args:
        request (GET): None

    Returns:
        HttpResponse: redirection to simulations or login
    """
    # check if user is logged in, redirect to login page if not
    if (not request.user.is_authenticated):
        return redirect('users:signin')
    # if its a GET request show the ipr form
    if (request.method == 'GET'):

        simulation = Simulation.objects.filter(url=simulation_url).first()
        if not simulation:
            owner = Role.objects.filter(name='owner').first()
            simulations = request.user.simulations.all()
            if owner:
                for simulation in simulations:
                    membership = simulation.membership_set.all().filter(role=owner).first()
                    if membership:
                        simulation.creator = membership.user

            messages.error(request, "simulation not found")
            return redirect('simulations:simulations')

        owner = Role.objects.filter(name='owner').first()
        membership = simulation.membership_set.all().filter(role=owner).first()
        if membership:
            simulation.creator = membership.user

        return render(request, 'simulations/well.html', {'simulation': simulation})

    # if its a POST request save data and show ipr form
    if (request.method == 'POST'):

        simulation = Simulation.objects.filter(url=simulation_url).first()
        if not simulation:
            owner = Role.objects.filter(name='owner').first()
            simulations = request.user.simulations.all()
            if owner:
                for simulation in simulations:
                    membership = simulation.membership_set.all().filter(role=owner).first()
                    if membership:
                        simulation.creator = membership.user

            messages.error(request, "simulation not found")
            return redirect('simulations:simulations')

        if simulation.has_well():
            # General Fields
            simulation.well.down_hole_pressure = request.POST.get('down_hole_pressure')
            simulation.well.productivity_flow_rate = request.POST.get('productivity_flow_rate')

            simulation.well.save()

        else:
            well = Well(
                # General Fields
                down_hole_pressure=request.POST.get('down_hole_pressure'),
                productivity_flow_rate=request.POST.get('productivity_flow_rate'),
                # Simulation Relation
                simulation=simulation
            )
            well.save()

        simulation.state = Simulation.SimulationState.Separator
        simulation.save()

        return redirect('/simulations/run/' + simulation.url + '/separator', {'simulation': simulation})


class RunGearBox(View):
    def get(self, request, simulation_url):
        if (not request.user.is_authenticated):
            return redirect('users:signin')

        simulation = Simulation.objects.filter(url=simulation_url).first()

        if not simulation:
            messages.error(request, "simulation not found")
            return redirect('simulations:simulations')

        # if simulation and simulation.has_surface_equipment():
        #     form = GearBoxFormPanel(
        #         initial={
        #             "power": simulation.gearbox.power,
        #         }
        #     )
        # else:
        form = GearBoxFormPanel(None)

        return render(
            request,
            "simulations/surface_equipment.html",
            {
                "simulation": simulation,
                "form": form
            }
        )

    def post(self, request, simulation_url):
        simulation = Simulation.objects.filter(url=simulation_url).first()
        form = GearBoxFormPanel(request.POST)

        if form.is_valid():
            inputs = dict(request.POST.items())
            inputs['simulation'] = simulation.pk
            # gearbox = UpdateGearBoxService.execute(inputs)
            return render(request, "simulations/surface_equipment.html", {"simulation": simulation, "form": form})

        else:
            return render(request, "simulations/surface_equipment.html", {"simulation": simulation, "form": form})


class RunMotor(View):
    def get(self, request, simulation_url):
        if (not request.user.is_authenticated):
            return redirect('users:signin')

        simulation = Simulation.objects.filter(url=simulation_url).first()

        if not simulation:
            messages.error(request, "simulation not found")
            return redirect('simulations:simulations')

        # if simulation and simulation.has_motor():
        #     form = MotorPanelForm(
        #         initial={
        #             "power_factor": simulation.motor.power_factor,
        #         }
        #     )
        # else:
        form = MotorPanelForm(None)

        return render(
            request,
            "simulations/motor.html",
            {
                "simulation": simulation,
                "form": form
            }
        )

    def post(self, request, simulation_url):
        simulation = Simulation.objects.filter(url=simulation_url).first()
        form = MotorPanelForm(request.POST)

        if form.is_valid():
            inputs = dict(request.POST.items())
            inputs['simulation'] = simulation.pk
            # motor = UpdateMotorService.execute(inputs)
            return render(
                request,
                "simulations/motor.html",
                {"simulation": simulation,
                 "form": form}
            )

        else:
            return render(
                request, "simulations/motor.html",
                {"simulation": simulation,
                 "form": form}
            )


class SimulationSettings(View):
    def get(self, request):
        return render(request, 'simulations/settings.html')

from .models import ExcelTestModel
from django.contrib import messages
from tablib import Dataset
from django.http import HttpResponse
from .forms import ExcelForm


class UploadFluid(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class UploadReservoir(View):

    def post(self, request):
        data_set = Dataset()
        new_person = request.FILES["myfile"]

        if not new_person.name.endswith("xlsx"):
            messages.info(request, "Wrong format")
            return render(request, "simulations/upload.html")

        imported_data = data_set.load(new_person.read(), format="xlsx")

        flag = False
        context = {}
        counter = 1
        for data in imported_data:
            form = ReservoirPanelForm(
                {
                    'flow_rate_vs_pressure': data[0],
                    'reservoir_pressure': data[1],
                    'reservoir_temperature': data[2],
                    'reservoir_type_option': data[3],
                }
            )
            for field in form:
                if field.errors:
                    context[str(counter)] = field.errors
                    counter = counter + 1
                    messages.error(request, field.errors)
                    flag = True
        if flag:
            return render(request, "simulations/upload.html", {'context': context})
        else:
            for data in imported_data:
                Reservoir.objects.create(
                    acentric_factors=data[0],
                    flow_rate_vs_pressure=data[1],
                    productivity_index=data[2],
                    reservoir_pressure=data[3],
                    reservoir_temperature=data[4],
                    reservoir_type_option=data[5],
                )
            return render(request, "simulations/upload.html")


class UploadWell(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class UploadSeperator(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class UploadPump(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class UploadRod(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class UploadPumpunit(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class UploadGearbox(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class UploadMotor(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class SimpleUpload(View):

    def get(self, request):
        return render(request, "simulations/upload.html")

    def post(self, request):
        data_set = Dataset()
        new_person = request.FILES["myfile"]

        if not new_person.name.endswith("xlsx"):
            messages.info(request, "Wrong format")
            return render(request, "simulations/upload.html")

        imported_data = data_set.load(new_person.read(), format="xlsx")

        flag = False
        context = {}
        counter = 1
        for data in imported_data:
            form = ExcelForm({'name': data[0]})
            for field in form:
                if field.errors:
                    context[str(counter)] = field.errors
                    counter = counter + 1
                    messages.error(request, field.errors)
                    flag = True
        if flag:
            return render(request, "simulations/upload.html", {'context': context})
        else:
            for data in imported_data:
                ExcelTestModel.objects.create(name=data[0])
            return render(request, "simulations/upload.html")


# implemented for development, must remove in production
def test(request):
    try:
        result = DummyModuleService.call_calculate(25, '/', 3)
        return render(request, 'simulations/test.html', {'heading': 'Good Work!', 'result': result})
    except ValidationError as v:
        return render(request, 'simulations/test.html', {'heading':v.message, 'result': v.errors, 'error': True})
    except ZeroDivisionError as z:
        return render(request, 'simulations/test.html', {'heading':z, 'error': True})






