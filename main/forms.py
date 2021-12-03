from .models import Option, Role, Unit, Permission
from django import forms


class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = [
            "display_name",
            "value",
            "field_name",
            "order_index",
        ]


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = [
            "display_name",
            "name",
            "permissions",
        ]


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = [
            "display_name",
            "equation",
            "is_base",
            "unit_type",
        ]


class PermissionForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = [
            "display_name",
            "name",
        ]
