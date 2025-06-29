"""
URL Configuration for Estágios System
Sistema de Gerenciamento de Estágios Supervisionados
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT customizado
    path('api/auth/login/',   TokenObtainPairView.as_view(),  name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(),     name='token_refresh'),
    path('api/auth/verify/',  TokenVerifyView.as_view(),      name='token_verify'),

    # JWT padrão (opcional)
    path('api/token/',         TokenObtainPairView.as_view(),  name='jwt_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(),     name='jwt_token_refresh'),

    # Rotas da API principal
    path('api/v1/', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# Personalização do Admin
admin.site.site_header = "Sistema de Estágios - Administração"
admin.site.site_title = "Estágios Admin"
admin.site.index_title = "Painel de Administração"
