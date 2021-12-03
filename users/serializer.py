from rest_framework import serializers
from .models import CustomUser


class SearchUserSerialize(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email"]

