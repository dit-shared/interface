from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from . import views
from django.conf.urls.static import static
from Frontend import settings

urlpatterns = [
	path('', views.redirect),
    path('admin/', admin.site.urls),
    path('auth/', include('Account.auth_urls')),
    path('account/', include('Account.account_urls')),
    path('dicom/', include('Dicom.urls')),
    path('series/', include('Slicer.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
