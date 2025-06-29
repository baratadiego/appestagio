"""
URLs para o app core - Sistema de Estágios
"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenVerifyView

from .views import (ConvenioViewSet, DocumentoViewSet, EstagiarioViewSet,
                    EstagioViewSet, EstatisticasView, MeView,
                    NotificacaoViewSet, RelatoriosView, NotificationViewSet,
                    MonthlyTrendsView, CourseDistributionView)

# Router para as APIs REST
router = DefaultRouter()

# Registrar os viewsets
router.register(r'estagiarios', EstagiarioViewSet, basename='estagiario')
router.register(r'convenios', ConvenioViewSet, basename='convenio')
router.register(r'estagios', EstagioViewSet, basename='estagio')
router.register(r'documentos', DocumentoViewSet, basename='documento')
router.register(r'notificacoes', NotificacaoViewSet, basename='notificacao')
router.register(r'notifications', NotificationViewSet, basename='notification')

app_name = 'core'

urlpatterns = [
    # API Routes
    path('', include(router.urls)),
    
    # Endpoint para estatísticas do painel administrativo
    path('estatisticas/', EstatisticasView.as_view(), name='estatisticas'),
    
    # Endpoints para relatórios
    path('relatorios/estagiarios/', RelatoriosView.as_view(), {'action': 'estagiarios'}, name='relatorio-estagiarios'),
    path('relatorios/estagios/', RelatoriosView.as_view(), {'action': 'estagios'}, name='relatorio-estagios'),
    
    # Endpoint pessoal do usuário
    path('me/', MeView.as_view(), name='me'),

    # Endpoint para verificação de token
    path('api/auth/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Novos endpoints para estatísticas
    path('statistics/monthly-trends/', MonthlyTrendsView.as_view(), name='monthly-trends'),
    path('statistics/course-distribution/', CourseDistributionView.as_view(), name='course-distribution'),
]

