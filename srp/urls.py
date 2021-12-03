from django.contrib import admin
from django.urls import include, path
# from django.conf.urls import url

urlpatterns = [
    path('', include('main.urls')),
    path('users/', include('users.urls')),
    path('simulations/', include('simulations.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]