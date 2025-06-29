"""
URLs para o app core - Sistema de Estágios
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EstagiarioViewSet, ConvenioViewSet, EstagioViewSet,
    DocumentoViewSet, NotificacaoViewSet, EstatisticasView,
    RelatoriosView
)

# Router para as APIs REST
router = DefaultRouter()

# Registrar os viewsets
router.register(r'estagiarios', EstagiarioViewSet, basename='estagiario')
router.register(r'convenios', ConvenioViewSet, basename='convenio')
router.register(r'estagios', EstagioViewSet, basename='estagio')
router.register(r'documentos', DocumentoViewSet, basename='documento')
router.register(r'notificacoes', NotificacaoViewSet, basename='notificacao')

app_name = 'core'

urlpatterns = [
    # API Routes
    path('', include(router.urls)),
  
]

