"""
Permissões personalizadas para o Sistema de Estágios
"""
from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permissão personalizada que permite apenas aos proprietários
    editar seus próprios objetos.
    """
    
    def has_object_permission(self, request, view, obj):
        # Permissões de leitura são permitidas para qualquer request,
        # então sempre permitimos requests GET, HEAD ou OPTIONS.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Permissões de escrita são apenas para o proprietário do objeto.
        return obj.usuario_upload == request.user


class IsAdminOrReadOnly(BasePermission):
    """
    Permissão personalizada que permite apenas aos administradores
    criar, editar ou deletar objetos. Usuários comuns podem apenas ler.
    """
    
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.is_staff


class IsEstagiarioOwnerOrAdmin(permissions.BasePermission):
    """
    Permissão que permite ao estagiário ver apenas seus próprios dados
    ou aos administradores ver todos os dados.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Administradores podem ver tudo
        if request.user.is_staff:
            return True
        
        # Estagiários podem ver apenas seus próprios dados
        if hasattr(obj, 'estagiario'):
            # Para objetos relacionados ao estagiário (como estágios, notificações)
            return obj.estagiario.email == request.user.email
        elif hasattr(obj, 'email'):
            # Para o próprio objeto estagiário
            return obj.email == request.user.email
        
        return False


class CanManageDocuments(permissions.BasePermission):
    """
    Permissão para gerenciar documentos.
    Administradores podem fazer tudo.
    Usuários comuns podem fazer upload e ver documentos dos próprios estágios.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Administradores podem fazer tudo
        if request.user.is_staff:
            return True
        
        # Para documentos, verificar se o usuário está relacionado ao estágio
        if hasattr(obj, 'estagio'):
            # Verificar se é o estagiário ou supervisor do estágio
            estagio = obj.estagio
            return (
                estagio.estagiario.email == request.user.email or
                estagio.supervisor_email == request.user.email
            )
        
        return False


class CanManageNotifications(permissions.BasePermission):
    """
    Permissão para gerenciar notificações.
    Administradores podem criar e gerenciar todas as notificações.
    Estagiários podem apenas ver e marcar como lidas suas próprias notificações.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Administradores podem fazer tudo
        if request.user.is_staff:
            return True
        
        # Estagiários podem apenas ver suas próprias notificações
        if hasattr(obj, 'estagiario'):
            # Apenas leitura e marcar como lida para estagiários
            if request.method in ['GET', 'POST'] and view.action in ['retrieve', 'marcar_lida']:
                return obj.estagiario.email == request.user.email
        
        return False


class IsStaffOrReadOnlyForOwner(permissions.BasePermission):
    """
    Permissão que permite:
    - Staff: CRUD completo
    - Proprietário: Apenas leitura
    - Outros: Sem acesso
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Staff pode fazer tudo
        if request.user.is_staff:
            return True
        
        # Proprietário pode apenas ler
        if request.method in permissions.SAFE_METHODS:
            if hasattr(obj, 'estagiario'):
                return obj.estagiario.email == request.user.email
            elif hasattr(obj, 'email'):
                return obj.email == request.user.email
        
        return False


class CanAccessStatistics(permissions.BasePermission):
    """
    Permissão para acessar estatísticas do sistema.
    Apenas administradores podem acessar.
    """
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.is_staff
        )


class CanGenerateReports(permissions.BasePermission):
    """
    Permissão para gerar relatórios.
    Apenas usuários staff podem gerar relatórios.
    """
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.is_staff
        )


class IsCoordenador(permissions.BasePermission):
    """
    Permissão que permite apenas aos usuários com papel de coordenador
    acessar a view.
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'COORDENADOR'


class IsSupervisor(permissions.BasePermission):
    """
    Permissão que permite apenas aos usuários com papel de supervisor
    acessar a view.
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'SUPERVISOR'


class IsAluno(permissions.BasePermission):
    """
    Permissão que permite apenas aos usuários com papel de aluno
    acessar a view.
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'ALUNO'


# Exemplo de uso em uma ViewSet:
# permission_classes = [IsCoordenador|IsSupervisor]

