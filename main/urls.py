from django.urls import include, path
from .views import api
from . import views

app_name = 'main'

# ui related urls
urlpatterns = [
    path('', views.index, name='index'),
    # path('simulations', views.simulations.list, name='simulations'),
    path('components', views.components, name='components'),
]

# api related urls
urlpatterns += [

    # Fluid urls:

    # Show fluid or create
    path('api/fluid/', api.FluidCreate.as_view(), name='create-fluid'),

    # Get a fluid by id
    path('api/fluid/<int:id>', api.get_fluid, name='get-fluid'),

    # update Fluid
    path('api/fluid/<int:id>', api.UpdateFluidById.as_view(), name='update-fluid'),

    # Delete a fluid by id
    path('api/fluid/<int:id>', api.delete_fluid, name='delete-fluid'),

    # IPR urls:

    # Show ipr objects or Create
    path('api/ipr/', api.IPRCreate.as_view(), name='create-ipr'),

    # Get a ipr by id
    path('api/ipr/<int:id>', api.get_ipr, name='get-ipr'),

    # update IPR
    path('api/ipr/<int:id>', api.UpdateIprById.as_view(), name='update-ipr'),

    # Delete a ipr by id
    path('api/ipr/<int:id>', api.delete_ipr, name='delete-ipr'),

    # Get options of a particular field
    path('api/options/<fields_names>', api.options),

    # Well urls:

     # Show well objects or Create
    path('api/well/', api.WellCreate.as_view(), name='create-well'),

    # Get a well by id
    path('api/well/<int:id>', api.get_well, name='get-well'),

    # update well
    path('api/well/<int:id>', api.UpdateWellById.as_view(), name='update-well'),

    # Delete a well by id
    path('api/well/<int:id>', api.delete_well, name='delete-well'),

    # Get options of a particular field
    path('api/options/<fields_names>', api.options),

    # Separator urls:

     # Show separator objects or Create
    path('api/separator/', api.SeparatorCreate.as_view(), name='create-separator'),

    # Get a separator by id
    path('api/separator/<int:id>', api.get_separator, name='get-separator'),

    # update separator
    path('api/separator/<int:id>', api.UpdateSeparatorById.as_view(), name='update-separator'),

    # Delete a separator by id
    path('api/separator/<int:id>', api.delete_separator, name='delete-separator'),

    # Get options of a particular field
    path('api/options/<fields_names>', api.options),

    # Get units
    path('api/units/<slug:unit_type>', api.units)
]