from django.core.exceptions import PermissionDenied
from simulations.models import Membership, Simulation, Role
from django.shortcuts import redirect
from django.contrib import messages

def user_is_simulation_owner(function):
    def wrap(request, *args, **kwargs):
        simulation = Simulation.objects.filter(url=kwargs['simulation_url'])
        if simulation:
            role = Role.objects.filter(name = 'owner').first()
            membership = Membership.objects.filter(user = request.user, simulation = simulation[0], role = role).first()
            
            if membership:
                return function(request, *args, **kwargs)
            else:
                raise PermissionDenied
        else:
            raise PermissionDenied

    
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
    
def user_has_access_to_simulation(function):
    def wrap(request, *args, **kwargs):
        simulation = Simulation.objects.filter(url=kwargs['simulation_url'])
        
        # if simulation is public, every user can view it
        if simulation.first().visibility == Simulation.SimulationVisibility.Public:
            return function(request, *args, **kwargs)

        if simulation:
            membership = Membership.objects.filter(user = request.user, simulation = simulation[0]).first()
            
            if membership:
                return function(request, *args, **kwargs)
            else:
                raise PermissionDenied
        else:
            raise PermissionDenied
    
    wrap.__doc__ = function.__doc__
    # wrap.__name__ = function.__name__
    return wrap

def valid_simulation(function):
    def wrap(request, *args, **kwargs):
        simulation = Simulation.objects.filter(url=kwargs['simulation_url']).first()
        
        # if simulation is public, every user can view it
        if simulation:
            return function(request, *args, **kwargs)
        else:
            return redirect('simulations:simulations')
    
    wrap.__doc__ = function.__doc__
    return wrap