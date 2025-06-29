"""
Views para o Sistema de Gerenciamento de Estágios Supervisionados
"""
import mimetypes
import os

from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from weasyprint import HTML
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (Convenio, Documento, Estagiario, Estagio,
                     EstatisticasSistema, Notificacao, Notification)
from .permissions import (CanAccessStatistics, CanGenerateReports,
                          CanManageDocuments, CanManageNotifications,
                          IsAdminOrReadOnly, IsAluno, IsCoordenador,
                          IsEstagiarioOwnerOrAdmin, IsSupervisor)
from .serializers import (ConvenioSerializer, DocumentoSerializer,
                          EstagiarioSerializer, EstagioSerializer,
                          EstatisticasSistemaSerializer,
                          NotificacaoCreateSerializer, NotificacaoSerializer,
                          RelatorioEstagiarioSerializer,
                          RelatorioEstagioSerializer, UserSerializer,
                          NotificationSerializer)


class EstagiarioViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciamento de estagiários"""
    
    queryset = Estagiario.objects.all()
    serializer_class = EstagiarioSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsCoordenador()]
        return [IsCoordenador() | IsSupervisor() | IsAluno()]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'curso']
    search_fields = ['nome', 'email', 'cpf', 'curso']
    ordering_fields = ['nome', 'data_cadastro', 'curso']
    ordering = ['nome']
    
    def get_queryset(self):
        """Otimiza as consultas com prefetch_related"""
        return self.queryset.prefetch_related('estagios', 'notificacoes')
    
    @action(detail=True, methods=['get'])
    def estagios(self, request, pk=None):
        """Retorna os estágios de um estagiário específico"""
        estagiario = self.get_object()
        estagios = estagiario.estagios.all().order_by('-data_inicio')
        serializer = EstagioSerializer(estagios, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def notificacoes(self, request, pk=None):
        """Retorna as notificações de um estagiário específico"""
        estagiario = self.get_object()
        notificacoes = estagiario.notificacoes.all().order_by('-data_envio')
        serializer = NotificacaoSerializer(notificacoes, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def ativos(self, request):
        """Retorna apenas estagiários ativos"""
        estagiarios_ativos = self.get_queryset().filter(status='ATIVO')
        page = self.paginate_queryset(estagiarios_ativos)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(estagiarios_ativos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        """Retorna estatísticas dos estagiários"""
        total = self.get_queryset().count()
        ativos = self.get_queryset().filter(status='ATIVO').count()
        inativos = total - ativos
        
        # Estatísticas por curso
        por_curso = self.get_queryset().values('curso').annotate(
            total=Count('id')
        ).order_by('-total')
        
        return Response({
            'total_estagiarios': total,
            'estagiarios_ativos': ativos,
            'estagiarios_inativos': inativos,
            'por_curso': list(por_curso)
        })


class ConvenioViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciamento de convênios"""
    
    queryset = Convenio.objects.all()
    serializer_class = ConvenioSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome_empresa', 'cnpj', 'responsavel']
    ordering_fields = ['nome_empresa', 'data_cadastro']
    ordering = ['nome_empresa']
    
    def get_queryset(self):
        """Otimiza as consultas com prefetch_related"""
        return self.queryset.prefetch_related('estagios')
    
    @action(detail=True, methods=['get'])
    def estagios(self, request, pk=None):
        """Retorna os estágios de um convênio específico"""
        convenio = self.get_object()
        estagios = convenio.estagios.all().order_by('-data_inicio')
        serializer = EstagioSerializer(estagios, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def ativos(self, request):
        """Retorna apenas convênios ativos"""
        convenios_ativos = self.get_queryset().filter(ativo=True)
        page = self.paginate_queryset(convenios_ativos)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(convenios_ativos, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def ativar(self, request, pk=None):
        """Ativa um convênio"""
        convenio = self.get_object()
        convenio.ativo = True
        convenio.save()
        serializer = self.get_serializer(convenio)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def desativar(self, request, pk=None):
        """Desativa um convênio"""
        convenio = self.get_object()
        convenio.ativo = False
        convenio.save()
        serializer = self.get_serializer(convenio)
        return Response(serializer.data)


class EstagioViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciamento de estágios"""
    
    queryset = Estagio.objects.all()
    serializer_class = EstagioSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'estagiario', 'convenio']
    search_fields = ['estagiario__nome', 'convenio__nome_empresa', 'supervisor']
    ordering_fields = ['data_inicio', 'data_fim', 'data_cadastro']
    ordering = ['-data_inicio']
    
    def get_queryset(self):
        """Otimiza as consultas com select_related"""
        return self.queryset.select_related('estagiario', 'convenio').prefetch_related('documentos')
    
    @action(detail=True, methods=['get'])
    def documentos(self, request, pk=None):
        """Retorna os documentos de um estágio específico"""
        estagio = self.get_object()
        documentos = estagio.documentos.all().order_by('-data_upload')
        serializer = DocumentoSerializer(documentos, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def em_andamento(self, request):
        """Retorna apenas estágios em andamento"""
        estagios_andamento = self.get_queryset().filter(status='EM_ANDAMENTO')
        page = self.paginate_queryset(estagios_andamento)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(estagios_andamento, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def finalizados(self, request):
        """Retorna apenas estágios finalizados"""
        estagios_finalizados = self.get_queryset().filter(status='FINALIZADO')
        page = self.paginate_queryset(estagios_finalizados)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(estagios_finalizados, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def vencendo(self, request):
        """Retorna estágios que estão vencendo nos próximos 30 dias"""
        hoje = timezone.now().date()
        data_limite = hoje + timezone.timedelta(days=30)
        
        estagios_vencendo = self.get_queryset().filter(
            status='EM_ANDAMENTO',
            data_fim__lte=data_limite,
            data_fim__gte=hoje
        )
        
        serializer = self.get_serializer(estagios_vencendo, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def finalizar(self, request, pk=None):
        """Finaliza um estágio"""
        estagio = self.get_object()
        if estagio.status != 'EM_ANDAMENTO':
            return Response(
                {'error': 'Apenas estágios em andamento podem ser finalizados.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        estagio.status = 'FINALIZADO'
        estagio.save()
        
        # Criar notificação para o estagiário
        Notificacao.objects.create(
            estagiario=estagio.estagiario,
            titulo='Estágio Finalizado',
            mensagem=f'Seu estágio na empresa {estagio.convenio.nome_empresa} foi finalizado.',
            tipo='INFO'
        )
        
        serializer = self.get_serializer(estagio)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def cancelar(self, request, pk=None):
        """Cancela um estágio"""
        estagio = self.get_object()
        if estagio.status not in ['EM_ANDAMENTO', 'SUSPENSO']:
            return Response(
                {'error': 'Apenas estágios em andamento ou suspensos podem ser cancelados.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        motivo = request.data.get('motivo', '')
        estagio.status = 'CANCELADO'
        if motivo:
            estagio.observacoes = f"{estagio.observacoes}\n\nMotivo do cancelamento: {motivo}".strip()
        estagio.save()
        
        # Criar notificação para o estagiário
        Notificacao.objects.create(
            estagiario=estagio.estagiario,
            titulo='Estágio Cancelado',
            mensagem=f'Seu estágio na empresa {estagio.convenio.nome_empresa} foi cancelado.',
            tipo='ALERTA'
        )
        
        serializer = self.get_serializer(estagio)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def download_term(self, request, pk=None):
        """Gera o termo de compromisso em PDF"""
        estagio = self.get_object()
        html_string = render_to_string('termo_compromisso.html', {'estagio': estagio})
        pdf_file = HTML(string=html_string).write_pdf()
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=termo_{estagio.id}.pdf'
        return response


class DocumentoViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciamento de documentos"""
    
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer
    permission_classes = [CanManageDocuments]
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo_documento', 'estagio']
    search_fields = ['descricao', 'estagio__estagiario__nome', 'estagio__convenio__nome_empresa']
    ordering_fields = ['data_upload', 'tipo_documento']
    ordering = ['-data_upload']
    
    def get_queryset(self):
        """Otimiza as consultas com select_related"""
        return self.queryset.select_related(
            'estagio__estagiario', 
            'estagio__convenio', 
            'usuario_upload'
        )
    
    def perform_create(self, serializer):
        """Define o usuário que fez o upload"""
        serializer.save(usuario_upload=self.request.user)
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """Faz o download de um documento"""
        documento = self.get_object()
        
        if not documento.arquivo:
            raise Http404("Arquivo não encontrado")
        
        try:
            # Determinar o tipo MIME
            content_type, _ = mimetypes.guess_type(documento.arquivo.path)
            if content_type is None:
                content_type = 'application/octet-stream'
            
            # Ler o arquivo
            with open(documento.arquivo.path, 'rb') as arquivo:
                response = HttpResponse(arquivo.read(), content_type=content_type)
                
            # Definir o nome do arquivo para download
            nome_arquivo = os.path.basename(documento.arquivo.name)
            response['Content-Disposition'] = f'attachment; filename="{nome_arquivo}"'
            
            return response
            
        except FileNotFoundError:
            raise Http404("Arquivo não encontrado no sistema")
    
    @action(detail=False, methods=['get'])
    def por_tipo(self, request):
        """Retorna documentos agrupados por tipo"""
        tipo = request.query_params.get('tipo')
        if not tipo:
            return Response(
                {'error': 'Parâmetro "tipo" é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        documentos = self.get_queryset().filter(tipo_documento=tipo)
        page = self.paginate_queryset(documentos)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(documentos, many=True)
        return Response(serializer.data)


class NotificacaoViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciamento de notificações"""
    
    queryset = Notificacao.objects.all()
    permission_classes = [CanManageNotifications]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['lida', 'tipo', 'estagiario']
    search_fields = ['titulo', 'mensagem', 'estagiario__nome']
    ordering_fields = ['data_envio', 'tipo']
    ordering = ['-data_envio']
    
    def get_queryset(self):
        """Otimiza as consultas com select_related"""
        return self.queryset.select_related('estagiario')
    
    def get_serializer_class(self):
        """Retorna o serializer apropriado baseado na ação"""
        if self.action == 'create':
            return NotificacaoCreateSerializer
        return NotificacaoSerializer
    
    @action(detail=True, methods=['post'])
    def marcar_lida(self, request, pk=None):
        """Marca uma notificação como lida"""
        notificacao = self.get_object()
        notificacao.marcar_como_lida()
        serializer = NotificacaoSerializer(notificacao, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def marcar_nao_lida(self, request, pk=None):
        """Marca uma notificação como não lida"""
        notificacao = self.get_object()
        notificacao.lida = False
        notificacao.data_leitura = None
        notificacao.save()
        serializer = NotificacaoSerializer(notificacao, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def nao_lidas(self, request):
        """Retorna apenas notificações não lidas"""
        notificacoes_nao_lidas = self.get_queryset().filter(lida=False)
        page = self.paginate_queryset(notificacoes_nao_lidas)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(notificacoes_nao_lidas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def marcar_todas_lidas(self, request):
        """Marca todas as notificações como lidas"""
        estagiario_id = request.data.get('estagiario_id')
        
        if estagiario_id:
            notificacoes = self.get_queryset().filter(
                estagiario_id=estagiario_id, 
                lida=False
            )
        else:
            notificacoes = self.get_queryset().filter(lida=False)
        
        count = 0
        for notificacao in notificacoes:
            notificacao.marcar_como_lida()
            count += 1
        
        return Response({
            'message': f'{count} notificação(ões) marcada(s) como lida(s).',
            'count': count
        })


class EstatisticasView(APIView):
    """View para estatísticas do sistema (painel administrativo)"""
    
    permission_classes = [CanAccessStatistics]
    
    def get(self, request):
        """Retorna as estatísticas do sistema"""
        # Atualizar estatísticas
        stats = EstatisticasSistema.calcular_estatisticas()
        
        # Estatísticas adicionais
        hoje = timezone.now().date()
        
        # Estágios vencendo nos próximos 30 dias
        estagios_vencendo = Estagio.objects.filter(
            status='EM_ANDAMENTO',
            data_fim__lte=hoje + timezone.timedelta(days=30),
            data_fim__gte=hoje
        ).count()
        
        # Documentos enviados no último mês
        documentos_mes = Documento.objects.filter(
            data_upload__gte=hoje - timezone.timedelta(days=30)
        ).count()
        
        # Notificações não lidas por tipo
        notificacoes_por_tipo = Notificacao.objects.filter(lida=False).values('tipo').annotate(
            total=Count('id')
        )
        
        # Estágios por status
        estagios_por_status = Estagio.objects.values('status').annotate(
            total=Count('id')
        )
        
        # Serializar as estatísticas principais
        serializer = EstatisticasSistemaSerializer(stats)
        
        # Combinar com estatísticas adicionais
        data = serializer.data
        data.update({
            'estagios_vencendo_30_dias': estagios_vencendo,
            'documentos_ultimo_mes': documentos_mes,
            'notificacoes_por_tipo': list(notificacoes_por_tipo),
            'estagios_por_status': list(estagios_por_status)
        })
        
        return Response(data)
    
    def post(self, request):
        """Força a atualização das estatísticas"""
        stats = EstatisticasSistema.calcular_estatisticas()
        serializer = EstatisticasSistemaSerializer(stats)
        return Response({
            'message': 'Estatísticas atualizadas com sucesso!',
            'data': serializer.data
        })


class RelatoriosView(APIView):
    """View para geração de relatórios"""
    
    permission_classes = [CanGenerateReports]
    
    @action(detail=False, methods=['post'])
    def estagiarios(self, request):
        """Gera relatório de estagiários"""
        serializer = RelatorioEstagiarioSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            
            # Filtrar estagiários
            queryset = Estagiario.objects.filter(
                data_cadastro__date__range=[
                    data['periodo_inicio'], 
                    data['periodo_fim']
                ]
            )
            
            if data['status'] != 'TODOS':
                queryset = queryset.filter(status=data['status'])
            
            if data.get('curso'):
                queryset = queryset.filter(curso__icontains=data['curso'])
            
            # Serializar resultados
            estagiarios_serializer = EstagiarioSerializer(queryset, many=True)
            
            return Response({
                'filtros': data,
                'total': queryset.count(),
                'estagiarios': estagiarios_serializer.data
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def estagios(self, request):
        """Gera relatório de estágios"""
        serializer = RelatorioEstagioSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            
            # Filtrar estágios
            queryset = Estagio.objects.filter(
                data_inicio__range=[
                    data['periodo_inicio'], 
                    data['periodo_fim']
                ]
            ).select_related('estagiario', 'convenio')
            
            if data['status'] != 'TODOS':
                queryset = queryset.filter(status=data['status'])
            
            if data.get('convenio'):
                queryset = queryset.filter(convenio_id=data['convenio'])
            
            # Serializar resultados
            estagios_serializer = EstagioSerializer(queryset, many=True)
            
            return Response({
                'filtros': data,
                'total': queryset.count(),
                'estagios': estagios_serializer.data
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

class MonthlyTrendsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        data = (
            Estagiario.objects
            .annotate(month=TruncMonth('data_cadastro'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )
        return Response(list(data))

class CourseDistributionView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        data = (
            Estagiario.objects
            .values('curso')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        return Response(list(data))

