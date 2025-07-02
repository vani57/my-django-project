from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse, JsonResponse

def home(request):
    return JsonResponse({
        'message': 'Hello from Django on Zappa!', 
        'status': 'success',
        'endpoints': {
            'admin': '/admin/',
            'api': '/api/',
            'health': '/health/'
        }
    })

def health_check(request):
    return JsonResponse({'status': 'ok', 'message': 'Django API is running!'})

urlpatterns = [
    path('', home, name='home'),  # Root URL handler
    path('admin/', admin.site.urls),
    path('api/', include('records.urls')),
    path('health/', health_check, name='health'),# Health check endpoint
]