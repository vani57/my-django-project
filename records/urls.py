from django.urls import path
from records.views import EmployeeView, CompanyView,  ProjectView, ProfileView
from django.urls import path,include
urlpatterns = [
    path('employee/', EmployeeView.as_view()),
    path('employee/<int:id>/', EmployeeView.as_view()),
    path('company/', CompanyView.as_view()),
    path('company/<int:id>/', CompanyView.as_view()),  
    path('project/', ProjectView.as_view()),
    path('project/<int:id>/', ProjectView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('profile/<int:id>/', ProfileView.as_view()),
]