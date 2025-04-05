from django.urls import path 
from . import views

urlpatterns = [
    path('', views.index, name='get'),
    path('generate', views.generate_from_files, name='post')
]
