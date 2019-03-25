from django.urls import path
from . import views

urlpatterns = [
    path('', views.app_render, name='account'),
    path('upload', views.uploadDicom, name='uploadDicom'),
]