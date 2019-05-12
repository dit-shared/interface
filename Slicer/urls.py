from django.urls import path
from . import views

urlpatterns = [
    path('view', views.image_series_view, name='image_series_view'),
    path('changeDocComment', views.changeDocComment, name='changeDocComment')
]