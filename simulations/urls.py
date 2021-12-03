from django.urls import path, include
from . import views

app_name = "simulations"

urlpatterns = [
    path('', views.simulations, name='simulations'),
    path('create/', views.create, name='create'),

    path('run/<slug:simulation_url>/', include([
        path('', views.run, name='run'),

        # Fluid for panel
        path('fluid', views.run_fluid, name='run.fluid'),
        path('reservoir', views.RunReservoir.as_view(), name="run.reservoir"),

        # path('ipr', views.run_ipr, name='run.ipr'),

        # Well form panel
        path('well', views.RunWell.as_view(), name='run.well'),
        path('separator', views.RunSeparator.as_view(), name='run.separator'),
        path('pump', views.RunPump.as_view(), name='run.pump'),

        # Rod form panel
        path('rod', views.RunRod.as_view(), name='run.rod'),

        # Pumpunit form panel
        path('pump_unit', views.RunPumpUnit.as_view(), name='run.pump_unit'),

        # Surface equipment form panel
        path('gearbox', views.RunGearBox.as_view(), name='run.gearbox'),
        path('motor', views.RunMotor.as_view(), name='run.motor'),
    ])),

    path('settings', views.SimulationSettings.as_view(), name='simulation-setting'),

    path('update/<str:simulation_url>/', views.update, name='update'),
    path('delete/<str:simulation_url>/', views.delete, name='delete'),
    path('upload/', views.SimpleUpload.as_view(), name="upload"),
    path('upload/', views.UploadFluid.as_view(), name="upload-fluid"),
    path('upload/', views.UploadReservoir.as_view(), name="upload-reservoir"),
    path('upload/', views.UploadWell.as_view(), name="upload-well"),
    path('upload/', views.UploadSeperator.as_view(), name="upload-seperator"),
    path('upload/', views.UploadPump.as_view(), name="upload-pump"),
    path('upload/', views.UploadRod.as_view(), name="upload-rod"),
    path('upload/', views.UploadPumpunit.as_view(), name="upload-pumpunit"),
    path('upload/', views.UploadGearbox.as_view(), name="upload-gearbox"),
    path('upload/', views.UploadMotor.as_view(), name="upload-motor"),

    # implemented for development, must remove in production
    path('test/', views.test, name='test'),
]

# api urls

from .api import create_fluid_apiview, create_design_apiview, delete_casing_tubing_apiview, update_casing_tubing_apiview, create_casing_tubing_apiview, get_list_of_casing_tubing_apiview, get_list_of_od_weight_id_apiview, RemoveMembershipSerializer, GetSimulationMembersSerializer, RemoveSimulationSerializer, GetSimulationSerializer, get_list_of_simulations_apiview, SimulationUpdateSerializer, MemberShipSaveSerializer

urlpatterns += [
    path("api/simulation-list/", get_list_of_simulations_apiview, name="simulation-list-serializer"),
    path("api/simulation-update/", SimulationUpdateSerializer.as_view(), name="simulation-update-serializer"),
    path("api/get-simulation/", GetSimulationSerializer.as_view(), name="get-simulation-serializer"),
    path("api/remove-simulation/", RemoveSimulationSerializer.as_view(), name="remove-simulation-serializer"),
    path("api/get-simulation-members/", GetSimulationMembersSerializer.as_view(), name="get-simulation-members-serializer"),
    path("api/remove-simulation-members/", RemoveMembershipSerializer.as_view(), name="remove-simulation-members-serializer"),
    path("api/add-user-to-simulation/", MemberShipSaveSerializer.as_view(), name="add-user-to-simulation"),

    path('api/get-od-weight-id/', get_list_of_od_weight_id_apiview, name='get-od-weight-id'),
    path('api/get-casing-tubing/', get_list_of_casing_tubing_apiview, name='get-casing-tubing'),
    path('api/create-casing-tubing/', create_casing_tubing_apiview, name='create-casing-tubing'),
    path('api/update-casing-tubing/', update_casing_tubing_apiview, name='update-casing-tubing'),
    path('api/delete-casing-tubing/', delete_casing_tubing_apiview, name='delete-casing-tubing'),
    path('api/create-design/', create_design_apiview, name='create-design'),
    path('api/create-fluid/', create_fluid_apiview, name='create-fluid'),
]


