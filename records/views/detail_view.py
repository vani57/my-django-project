#detail_views.py
from .base import BaseModelView
from django_filters.rest_framework import DjangoFilterBackend
from records.models import Employee, Company, Project, Profile
from records.serializers import EmployeeSerializer, CompanySerializer, ProjectSerializer, ProfileSerializer

class EmployeeView(BaseModelView):
    model = Employee
    serializer_class = EmployeeSerializer
    #filter_backends = [DjangoFilterBackend]
    

class CompanyView(BaseModelView):
    model = Company
    serializer_class = CompanySerializer
    

class ProjectView(BaseModelView):
    model = Project
    serializer_class = ProjectSerializer
    
class ProfileView(BaseModelView):
    model = Profile
    serializer_class = ProfileSerializer