from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager
from simulations.models import Simulation, Membership, Fluid, Well, IPR, SeparatorSize, Separator, Rod, PumpUnit, Gearbox


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    simulations = models.ManyToManyField(Simulation, through=Membership)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def full_name(self):
        return self.first_name + " " + self.last_name