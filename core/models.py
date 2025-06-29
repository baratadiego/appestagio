"""
Modelos para o Sistema de Gerenciamento de Estágios Supervisionados
"""
import os

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


def upload_documento_path(instance, filename):
    """Função para definir o caminho de upload dos documentos"""
    return f'documentos/{instance.estagio.estagiario.nome}/{filename}'


class User(AbstractUser):
    """Modelo para usuários do sistema (inclui estagiários, supervisores e coordenadores)"""
    
    ROLE_CHOICES = (
        ('COORDENADOR', 'Coordenador'),
        ('SUPERVISOR', 'Supervisor'),
        ('ALUNO', 'Aluno'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='ALUNO')


class Estagiario(models.Model):
    """Modelo para cadastro de estagiários"""
    
    STATUS_CHOICES = [
        ('ATIVO', 'Ativo'),
        ('INATIVO', 'Inativo'),
    ]
    
    # Validador para CPF (formato: 000.000.000-00)
    cpf_validator = RegexValidator(
        regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
        message='CPF deve estar no formato: 000.000.000-00'
    )
    
    # Validador para telefone (formato: (00) 00000-0000)
    telefone_validator = RegexValidator(
        regex=r'^\(\d{2}\) \d{4,5}-\d{4}$',
        message='Telefone deve estar no formato: (00) 00000-0000'
    )
    
    nome = models.CharField(max_length=200, verbose_name='Nome Completo')
    email = models.EmailField(unique=True, verbose_name='E-mail')
    telefone = models.CharField(
        max_length=15, 
        validators=[telefone_validator],
        verbose_name='Telefone'
    )
    curso = models.CharField(max_length=100, verbose_name='Curso')
    periodo = models.CharField(max_length=20, verbose_name='Período')
    cpf = models.CharField(
        max_length=14, 
        unique=True,
        validators=[cpf_validator],
        verbose_name='CPF'
    )
    data_nascimento = models.DateField(verbose_name='Data de Nascimento')
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='ATIVO',
        verbose_name='Status'
    )
    
    # Campos de controle
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name='Última Atualização')
    
    class Meta:
        verbose_name = 'Estagiário'
        verbose_name_plural = 'Estagiários'
        ordering = ['nome']
        
    def __str__(self):
        return f"{self.nome} - {self.curso}"
    
    @property
    def idade(self):
        """Calcula a idade do estagiário"""
        today = timezone.now().date()
        return today.year - self.data_nascimento.year - (
            (today.month, today.day) < (self.data_nascimento.month, self.data_nascimento.day)
        )


class Convenio(models.Model):
    """Modelo para registro de convênios com empresas"""
    
    # Validador para CNPJ (formato: 00.000.000/0000-00)
    cnpj_validator = RegexValidator(
        regex=r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$',
        message='CNPJ deve estar no formato: 00.000.000/0000-00'
    )
    
    # Validador para telefone
    telefone_validator = RegexValidator(
        regex=r'^\(\d{2}\) \d{4,5}-\d{4}$',
        message='Telefone deve estar no formato: (00) 00000-0000'
    )
    
    nome_empresa = models.CharField(max_length=200, verbose_name='Nome da Empresa')
    cnpj = models.CharField(
        max_length=18, 
        unique=True,
        validators=[cnpj_validator],
        verbose_name='CNPJ'
    )
    endereco = models.TextField(verbose_name='Endereço')
    telefone = models.CharField(
        max_length=15, 
        validators=[telefone_validator],
        verbose_name='Telefone'
    )
    responsavel = models.CharField(max_length=200, verbose_name='Responsável')
    email_responsavel = models.EmailField(
        blank=True, 
        null=True, 
        verbose_name='E-mail do Responsável'
    )
    
    # Campos de controle
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name='Última Atualização')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    
    class Meta:
        verbose_name = 'Convênio'
        verbose_name_plural = 'Convênios'
        ordering = ['nome_empresa']
        
    def __str__(self):
        return f"{self.nome_empresa} - {self.responsavel}"


class Estagio(models.Model):
    """Modelo para acompanhamento de estágios"""
    
    STATUS_CHOICES = [
        ('EM_ANDAMENTO', 'Em Andamento'),
        ('FINALIZADO', 'Finalizado'),
        ('CANCELADO', 'Cancelado'),
        ('SUSPENSO', 'Suspenso'),
    ]
    
    estagiario = models.ForeignKey(
        Estagiario, 
        on_delete=models.CASCADE,
        related_name='estagios',
        verbose_name='Estagiário'
    )
    convenio = models.ForeignKey(
        Convenio, 
        on_delete=models.CASCADE,
        related_name='estagios',
        verbose_name='Convênio'
    )
    supervisor = models.CharField(max_length=200, verbose_name='Supervisor')
    supervisor_email = models.EmailField(
        blank=True, 
        null=True, 
        verbose_name='E-mail do Supervisor'
    )
    carga_horaria = models.PositiveIntegerField(verbose_name='Carga Horária (horas)')
    data_inicio = models.DateField(verbose_name='Data de Início')
    data_fim = models.DateField(verbose_name='Data de Fim')
    status = models.CharField(
        max_length=15, 
        choices=STATUS_CHOICES, 
        default='EM_ANDAMENTO',
        verbose_name='Status'
    )
    observacoes = models.TextField(blank=True, verbose_name='Observações')
    
    # Campos de controle
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name='Última Atualização')
    
    class Meta:
        verbose_name = 'Estágio'
        verbose_name_plural = 'Estágios'
        ordering = ['-data_inicio']
        
    def __str__(self):
        return f"{self.estagiario.nome} - {self.convenio.nome_empresa}"
    
    @property
    def duracao_dias(self):
        """Calcula a duração do estágio em dias"""
        return (self.data_fim - self.data_inicio).days
    
    @property
    def dias_restantes(self):
        """Calcula quantos dias restam para o fim do estágio"""
        if self.status == 'EM_ANDAMENTO':
            hoje = timezone.now().date()
            if hoje <= self.data_fim:
                return (self.data_fim - hoje).days
        return 0


class Documento(models.Model):
    """Modelo para documentação e assinaturas"""
    
    TIPO_DOCUMENTO_CHOICES = [
        ('TERMO_COMPROMISSO', 'Termo de Compromisso'),
        ('PLANO_ESTAGIO', 'Plano de Estágio'),
        ('RELATORIO', 'Relatório'),
        ('AVALIACAO', 'Avaliação'),
        ('OUTROS', 'Outros'),
    ]
    
    estagio = models.ForeignKey(
        Estagio, 
        on_delete=models.CASCADE,
        related_name='documentos',
        verbose_name='Estágio'
    )
    tipo_documento = models.CharField(
        max_length=20, 
        choices=TIPO_DOCUMENTO_CHOICES,
        verbose_name='Tipo de Documento'
    )
    arquivo = models.FileField(
        upload_to=upload_documento_path,
        verbose_name='Arquivo'
    )
    descricao = models.CharField(
        max_length=200, 
        blank=True,
        verbose_name='Descrição'
    )
    
    # Campos de controle
    data_upload = models.DateTimeField(auto_now_add=True, verbose_name='Data de Upload')
    usuario_upload = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Usuário que fez o Upload'
    )
    
    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'
        ordering = ['-data_upload']
        
    def __str__(self):
        return f"{self.get_tipo_documento_display()} - {self.estagio}"
    
    def delete(self, *args, **kwargs):
        """Override do delete para remover o arquivo do sistema"""
        if self.arquivo:
            if os.path.isfile(self.arquivo.path):
                os.remove(self.arquivo.path)
        super().delete(*args, **kwargs)


class Notificacao(models.Model):
    """Modelo para notificações e alertas"""
    
    TIPO_NOTIFICACAO_CHOICES = [
        ('INFO', 'Informação'),
        ('ALERTA', 'Alerta'),
        ('URGENTE', 'Urgente'),
    ]
    
    estagiario = models.ForeignKey(
        Estagiario, 
        on_delete=models.CASCADE,
        related_name='notificacoes',
        verbose_name='Estagiário'
    )
    titulo = models.CharField(max_length=200, verbose_name='Título')
    mensagem = models.TextField(verbose_name='Mensagem')
    tipo = models.CharField(
        max_length=10, 
        choices=TIPO_NOTIFICACAO_CHOICES, 
        default='INFO',
        verbose_name='Tipo'
    )
    lida = models.BooleanField(default=False, verbose_name='Lida')
    
    # Campos de controle
    data_envio = models.DateTimeField(auto_now_add=True, verbose_name='Data de Envio')
    data_leitura = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name='Data de Leitura'
    )
    
    class Meta:
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'
        ordering = ['-data_envio']
        indexes = [
            models.Index(fields=['estagiario', 'lida']),
        ]
        
    def __str__(self):
        return f"{self.titulo} - {self.estagiario.nome}"
    
    def marcar_como_lida(self):
        """Marca a notificação como lida"""
        if not self.lida:
            self.lida = True
            self.data_leitura = timezone.now()
            self.save()


class EstatisticasSistema(models.Model):
    """Modelo para armazenar estatísticas do sistema (cache)"""
    
    data_calculo = models.DateTimeField(auto_now=True, verbose_name='Data do Cálculo')
    total_estagiarios = models.PositiveIntegerField(default=0, verbose_name='Total de Estagiários')
    estagiarios_ativos = models.PositiveIntegerField(default=0, verbose_name='Estagiários Ativos')
    total_estagios = models.PositiveIntegerField(default=0, verbose_name='Total de Estágios')
    estagios_em_andamento = models.PositiveIntegerField(default=0, verbose_name='Estágios em Andamento')
    total_convenios = models.PositiveIntegerField(default=0, verbose_name='Total de Convênios')
    convenios_ativos = models.PositiveIntegerField(default=0, verbose_name='Convênios Ativos')
    total_documentos = models.PositiveIntegerField(default=0, verbose_name='Total de Documentos')
    notificacoes_nao_lidas = models.PositiveIntegerField(default=0, verbose_name='Notificações Não Lidas')
    
    class Meta:
        verbose_name = 'Estatísticas do Sistema'
        verbose_name_plural = 'Estatísticas do Sistema'
        
    def __str__(self):
        return f"Estatísticas - {self.data_calculo.strftime('%d/%m/%Y %H:%M')}"
    
    @classmethod
    def calcular_estatisticas(cls):
        """Método para calcular e atualizar as estatísticas"""
        stats, created = cls.objects.get_or_create(id=1)
        
        stats.total_estagiarios = Estagiario.objects.count()
        stats.estagiarios_ativos = Estagiario.objects.filter(status='ATIVO').count()
        stats.total_estagios = Estagio.objects.count()
        stats.estagios_em_andamento = Estagio.objects.filter(status='EM_ANDAMENTO').count()
        stats.total_convenios = Convenio.objects.count()
        stats.convenios_ativos = Convenio.objects.filter(ativo=True).count()
        stats.total_documentos = Documento.objects.count()
        stats.notificacoes_nao_lidas = Notificacao.objects.filter(lida=False).count()
        
        stats.save()
        return stats


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    due_date = models.DateTimeField(null=True, blank=True)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.message[:40]}"

