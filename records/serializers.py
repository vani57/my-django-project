from rest_framework import serializers
from .models import Employee, Profile, Company, Project

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())

    class Meta:
        model = Employee
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    employees = EmployeeSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())

    class Meta:
        model = Profile 
        fields = '__all__'
