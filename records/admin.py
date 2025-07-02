from django.contrib import admin
from .models import Company, Employee, Profile, Project

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name', 'location')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'department', 'join_date', 'company')
    list_filter = ('company', 'department')
    search_fields = ('name', 'email')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('employee', 'linkedin')
    search_fields = ('employee__name',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    filter_horizontal = ('employees',)  # Nice widget for ManyToMany

