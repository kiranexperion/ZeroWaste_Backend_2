from rest_framework import serializers

from .models import wards, wastes, roles, wastecollector, employee, collectionstatus

class wardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = wards
        fields = ('__all__')

class wastesSerializer(serializers.ModelSerializer):
    class Meta:
        model = wastes
        fields = ('__all__')

class rolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = roles
        fields = ('__all__')

class wastecollectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = wastecollector
        fields = ('__all__')

class employeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = employee
        fields = ('__all__')

class collectionstatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = collectionstatus
        fields = ('__all__')