from django.shortcuts import redirect, render
from main.models import Role

def index(request):
    return redirect('users:dashboard')


def components(request):
    return render(request, 'pages/components.html')

def dashboard(request):
    if(request.method == 'POST'):
        name = request.POST.get('name')
        description = request.POST.get('description')
        visibility = request.POST.get('visibility')
        simulation = Simulation(name=name, description=description, visibility=visibility)
        simulation.save()

    if(not request.user.is_authenticated):
        return redirect('users:signin')

    owner = Role.objects.filter(name = 'owner').first()
    simulations = request.user.simulations.order_by('-id')[:4]
    if owner:
        for simulation in simulations:
            membership = simulation.membership_set.all().filter(role = owner).first()
            if membership:
                simulation.creator = membership.user

    return render(request, 'dashboard.html', { 'simulations' : simulations })