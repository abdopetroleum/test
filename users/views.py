from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.contrib import messages
from simulations.models import Role, Simulation


def signin(request):
    """handles the login process

    Args:
        request (GET,POST): username, password

    Returns:
        HttpResponse: login page
    """
    # check if user already signed in
    if (request.user.is_authenticated):
        return redirect('users:dashboard')
    # if its a GET request show the login form
    if (request.method == 'GET'):
        return render(request, 'layouts/signin.html')
    # if its a POST request test the credential
    elif (request.method == 'POST'):
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            # if the credentials are valid login the user
            login(request, user)
            # redirect to home
            return redirect('users:dashboard')
        else:
            # the credentials are invalid
            messages.error(request, "Wrong username or password.")
            return redirect('users:signin')


def signout(request):
    auth_logout(request)
    return redirect('users:signin')


def dashboard(request):
    if (request.method == 'POST'):
        name = request.POST.get('name')
        description = request.POST.get('description')
        visibility = request.POST.get('visibility')
        simulation = Simulation(name=name, description=description, visibility=visibility)
        simulation.save()

    if (not request.user.is_authenticated):
        return redirect('users:signin')

    owner = Role.objects.filter(name='owner').first()
    simulations = request.user.simulations.order_by('-id')[:4]
    if owner:
        for simulation in simulations:
            membership = simulation.membership_set.all().filter(role=owner).first()
            if membership:
                simulation.creator = membership.user

    return render(request, 'dashboard.html', {'simulations': simulations})
