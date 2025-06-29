"""
Configuração do painel administrativo para o Sistema de Estágios
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    Estagiario, Convenio, Estagio, Documento, 
    Notificacao, EstatisticasSistema
)


@admin.register(Estagiario)
class EstagiarioAdmin(admin.ModelAdmin):
    """Configuração do admin para Estagiários"""
    
    list_display = [
        'nome', 'email', 'curso', 'periodo', 'status', 
        'idade_display', 'data_cadastro'
    ]
    list_filter = ['status', 'curso', 'data_cadastro']
    search_fields = ['nome', 'email', 'cpf', 'curso']
    readonly_fields = ['data_cadastro', 'data_atualizacao', 'idade_display']
    
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('nome', 'email', 'telefone', 'cpf', 'data_nascimento')
        }),
        ('Informações Acadêmicas', {
            'fields': ('curso', 'periodo')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Controle', {
            'fields': ('data_cadastro', 'data_atualizacao', 'idade_display'),
            'classes': ('collapse',)
        }),
    )
    
    def idade_display(self, obj):
        """Exibe a idade do estagiário"""
        return f"{obj.idade} anos"
    idade_display.short_description = 'Idade'
    
    def get_queryset(self, request):
        """Otimiza as consultas"""
        return super().get_queryset(request).select_related()


@admin.register(Convenio)
class ConvenioAdmin(admin.ModelAdmin):
    """Configuração do admin para Convênios"""
    
    list_display = [
        'nome_empresa', 'responsavel', 'telefone', 
        'ativo', 'total_estagios', 'data_cadastro'
    ]
    list_filter = ['ativo', 'data_cadastro']
    search_fields = ['nome_empresa', 'cnpj', 'responsavel']
    readonly_fields = ['data_cadastro', 'data_atualizacao', 'total_estagios']
    
    fieldsets = (
        ('Informações da Empresa', {
            'fields': ('nome_empresa', 'cnpj', 'endereco', 'telefone')
        }),
        ('Responsável', {
            'fields': ('responsavel', 'email_responsavel')
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
        ('Estatísticas', {
            'fields': ('total_estagios',),
            'classes': ('collapse',)
        }),
        ('Controle', {
            'fields': ('data_cadastro', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )
    
    def total_estagios(self, obj):
        """Exibe o total de estágios da empresa"""
        total = obj.estagios.count()
        if total > 0:
            url = reverse('admin:core_estagio_changelist') + f'?convenio__id__exact={obj.id}'
            return format_html('<a href="{}">{} estágios</a>', url, total)
        return "0 estágios"
    total_estagios.short_description = 'Total de Estágios'


@admin.register(Estagio)
class EstagioAdmin(admin.ModelAdmin):
    """Configuração do admin para Estágios"""
    
    list_display = [
        'estagiario', 'convenio', 'supervisor', 'status',
        'data_inicio', 'data_fim', 'dias_restantes_display'
    ]
    list_filter = ['status', 'data_inicio', 'data_fim']
    search_fields = [
        'estagiario__nome', 'convenio__nome_empresa', 
        'supervisor'
    ]
    readonly_fields = [
        'data_cadastro', 'data_atualizacao', 
        'duracao_dias_display', 'dias_restantes_display'
    ]
    
    fieldsets = (
        ('Participantes', {
            'fields': ('estagiario', 'convenio')
        }),
        ('Supervisão', {
            'fields': ('supervisor', 'supervisor_email')
        }),
        ('Período e Carga Horária', {
            'fields': ('data_inicio', 'data_fim', 'carga_horaria')
        }),
        ('Status e Observações', {
            'fields': ('status', 'observacoes')
        }),
        ('Estatísticas', {
            'fields': ('duracao_dias_display', 'dias_restantes_display'),
            'classes': ('collapse',)
        }),
        ('Controle', {
            'fields': ('data_cadastro', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )
    
    def duracao_dias_display(self, obj):
        """Exibe a duração do estágio em dias"""
        return f"{obj.duracao_dias} dias"
    duracao_dias_display.short_description = 'Duração'
    
    def dias_restantes_display(self, obj):
        """Exibe os dias restantes do estágio"""
        dias = obj.dias_restantes
        if dias > 0:
            return format_html('<span style="color: green;">{} dias</span>', dias)
        elif obj.status == 'EM_ANDAMENTO':
            return format_html('<span style="color: red;">Vencido</span>')
        return '-'
    dias_restantes_display.short_description = 'Dias Restantes'
    
    def get_queryset(self, request):
        """Otimiza as consultas"""
        return super().get_queryset(request).select_related(
            'estagiario', 'convenio'
        )


@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    """Configuração do admin para Documentos"""
    
    list_display = [
        'tipo_documento', 'estagio', 'descricao', 
        'arquivo_link', 'data_upload', 'usuario_upload'
    ]
    list_filter = ['tipo_documento', 'data_upload']
    search_fields = [
        'estagio__estagiario__nome', 
        'estagio__convenio__nome_empresa',
        'descricao'
    ]
    readonly_fields = ['data_upload', 'usuario_upload', 'arquivo_link']
    
    fieldsets = (
        ('Documento', {
            'fields': ('estagio', 'tipo_documento', 'descricao')
        }),
        ('Arquivo', {
            'fields': ('arquivo', 'arquivo_link')
        }),
        ('Controle', {
            'fields': ('data_upload', 'usuario_upload'),
            'classes': ('collapse',)
        }),
    )
    
    def arquivo_link(self, obj):
        """Cria link para download do arquivo"""
        if obj.arquivo:
            return format_html(
                '<a href="{}" target="_blank">📄 Baixar Arquivo</a>',
                obj.arquivo.url
            )
        return "Nenhum arquivo"
    arquivo_link.short_description = 'Arquivo'
    
    def save_model(self, request, obj, form, change):
        """Salva o usuário que fez o upload"""
        if not change:  # Novo documento
            obj.usuario_upload = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        """Otimiza as consultas"""
        return super().get_queryset(request).select_related(
            'estagio__estagiario', 'estagio__convenio', 'usuario_upload'
        )


@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    """Configuração do admin para Notificações"""
    
    list_display = [
        'titulo', 'estagiario', 'tipo', 'lida', 
        'data_envio', 'data_leitura'
    ]
    list_filter = ['tipo', 'lida', 'data_envio']
    search_fields = ['titulo', 'mensagem', 'estagiario__nome']
    readonly_fields = ['data_envio', 'data_leitura']
    
    fieldsets = (
        ('Notificação', {
            'fields': ('estagiario', 'titulo', 'mensagem', 'tipo')
        }),
        ('Status', {
            'fields': ('lida', 'data_leitura')
        }),
        ('Controle', {
            'fields': ('data_envio',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['marcar_como_lida', 'marcar_como_nao_lida']
    
    def marcar_como_lida(self, request, queryset):
        """Ação para marcar notificações como lidas"""
        count = 0
        for notificacao in queryset:
            if not notificacao.lida:
                notificacao.marcar_como_lida()
                count += 1
        
        self.message_user(
            request, 
            f'{count} notificação(ões) marcada(s) como lida(s).'
        )
    marcar_como_lida.short_description = "Marcar como lida"
    
    def marcar_como_nao_lida(self, request, queryset):
        """Ação para marcar notificações como não lidas"""
        count = queryset.filter(lida=True).update(
            lida=False, 
            data_leitura=None
        )
        self.message_user(
            request, 
            f'{count} notificação(ões) marcada(s) como não lida(s).'
        )
    marcar_como_nao_lida.short_description = "Marcar como não lida"
    
    def get_queryset(self, request):
        """Otimiza as consultas"""
        return super().get_queryset(request).select_related('estagiario')


@admin.register(EstatisticasSistema)
class EstatisticasSistemaAdmin(admin.ModelAdmin):
    """Configuração do admin para Estatísticas do Sistema"""
    
    list_display = [
        'data_calculo', 'total_estagiarios', 'estagios_em_andamento',
        'convenios_ativos', 'total_documentos'
    ]
    readonly_fields = [
        'data_calculo', 'total_estagiarios', 'estagiarios_ativos',
        'total_estagios', 'estagios_em_andamento', 'total_convenios',
        'convenios_ativos', 'total_documentos', 'notificacoes_nao_lidas'
    ]
    
    fieldsets = (
        ('Estagiários', {
            'fields': ('total_estagiarios', 'estagiarios_ativos')
        }),
        ('Estágios', {
            'fields': ('total_estagios', 'estagios_em_andamento')
        }),
        ('Convênios', {
            'fields': ('total_convenios', 'convenios_ativos')
        }),
        ('Documentos e Notificações', {
            'fields': ('total_documentos', 'notificacoes_nao_lidas')
        }),
        ('Controle', {
            'fields': ('data_calculo',)
        }),
    )
    
    actions = ['atualizar_estatisticas']
    
    def atualizar_estatisticas(self, request, queryset):
        """Ação para atualizar as estatísticas"""
        EstatisticasSistema.calcular_estatisticas()
        self.message_user(request, 'Estatísticas atualizadas com sucesso!')
    atualizar_estatisticas.short_description = "Atualizar estatísticas"
    
    def has_add_permission(self, request):
        """Impede a criação manual de estatísticas"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Impede a exclusão de estatísticas"""
        return False

