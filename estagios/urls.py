"""
URL Configuration for Estágios System
Sistema de Gerenciamento de Estágios Supervisionados
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.http import HttpResponse

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API Routes
    path('api/v1/', include('core.urls')),
    
    # Home
    path('', lambda request: HttpResponse("Sistema de Estágios - API"), name='home'),
]

# Servir arquivos de mídia em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Configurar títulos do admin
admin.site.site_header = "Sistema de Estágios - Administração"
admin.site.site_title = "Estágios Admin"
admin.site.index_title = "Painel de Administração"

