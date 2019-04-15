from django.urls import path
from . import views

urlpatterns = [
    path('', views.account, name='account'),
    path('upload', views.upload, name='upload'),
    path('predict', views.predict_view, name='predict'),
    path('view', views.view, name='view'),
    path('predict/get', views.predict, name='predict'),
    path('feedback', views.feedback, name='feedback'),
    path('uploadAva', views.uploadAva, name='uploadAva'),
    path('changeAccount', views.changeAccount, name='changeAccount'),
    # temporary handlers
    path('encpass', views.encPasswd, name='encPasswd'),
]