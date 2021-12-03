from django.db import models


class Option(models.Model):
    #Field Name Of The Option, For Example Oil Correlation
    field_name = models.CharField(max_length=50, db_index=True)
    #Display Name Of The Option, For Example Matthew & Russell
    display_name = models.CharField(max_length=50)
    #Actual Value Of The Option, For Example Matthew_russell
    value = models.CharField(max_length=50)
    #Display Order Index
    order_index = models.IntegerField()
    #Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order_index']

    def __str__(self):
        return self.display_name

class Unit(models.Model):
    #The Type Of The Unit, For Example Pressure, Temperture, ...
    unit_type = models.CharField(max_length=50, db_index=True)
    #Display Name
    display_name = models.CharField(max_length=50)
    #Is The Base Unit Of Calculating Other Similar Units?
    is_base = models.BooleanField(default=False)
    #The Equation Of Calculating This Unit Depending On It'S Base Unit
    #For Example °c + 273.15 = K
    #The Equation Will Be X+273.15 For The Given Example
    equation = models.CharField(max_length=50)
    #the units are predefined by the developer, so no need for timestaps

class Permission(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    display_name = models.CharField(max_length=50)
    #the permissions are predefined by the developer, so no need for timestaps

class Role(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    display_name = models.CharField(max_length=50)
    permissions = models.ManyToManyField(Permission, null = True)
    #Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

