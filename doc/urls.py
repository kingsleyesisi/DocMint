"""
DocMint URLs Configuration
"""
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

# API v1 patterns
api_v1_patterns = [
    # Health check
    path('health/', views.health_check, name='health_check'),
    
    # README generation endpoints
    path('generate/', views.generate_from_prompt, name='generate_from_prompt'),
    path('generate-from-files/', views.generate_from_files, name='generate_from_files'),
    
    # Utility endpoints
    path('formats/', views.get_supported_formats, name='supported_formats'),
    path('validate/', views.validate_project, name='validate_project'),
]

# Main URL patterns
urlpatterns = [
    # API v1 routes
    path('api/', include(api_v1_patterns)),
    path('api/v1/', include(api_v1_patterns)),  # Versioned API
    
    # Legacy endpoints (for backward compatibility)
    path('test/', views.test, name='legacy_test'),
    path('', views.index, name='legacy_index'),  # Root endpoint for basic info
    
    # Health check at root for load balancers
    path('health/', views.health_check, name='root_health'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)