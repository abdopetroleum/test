from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('dashboard/', views.dashboard, name='dashboard'),
]

from .api import SearchUserSerializer

urlpatterns += [
    path("api/search-user/", SearchUserSerializer.as_view(), name="search-user")
]