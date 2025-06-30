"""
Serializers para o Sistema de Gerenciamento de Estágios Supervisionados
"""
import re

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers

from .models import (Convenio, Documento, Estagiario, Estagio,
                     EstatisticasSistema, Notificacao, Notification)

User = get_user_model()


class EstagiarioSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Estagiário"""
    
    idade = serializers.ReadOnlyField()
    total_estagios = serializers.SerializerMethodField()
    
    class Meta:
        model = Estagiario
        fields = [
            'id', 'nome', 'email', 'telefone', 'curso', 'periodo',
            'cpf', 'data_nascimento', 'status', 'idade', 'total_estagios',
            'data_cadastro', 'data_atualizacao'
        ]
        read_only_fields = ['data_cadastro', 'data_atualizacao']
    
    def get_total_estagios(self, obj):
        """Retorna o total de estágios do estagiário"""
        return obj.estagios.count()
    
    def validate_cpf(self, value):
        """Validação personalizada para CPF"""
        if not re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', value):
            raise serializers.ValidationError(
                'CPF deve estar no formato: 000.000.000-00'
            )
        return value
    
    def validate_telefone(self, value):
        """Validação personalizada para telefone"""
        if not re.match(r'^\(\d{2}\) \d{4,5}-\d{4}$', value):
            raise serializers.ValidationError(
                'Telefone deve estar no formato: (00) 00000-0000'
            )
        return value
    
    def validate_data_nascimento(self, value):
        """Validação para data de nascimento"""
        hoje = timezone.now().date()
        idade = hoje.year - value.year - ((hoje.month, hoje.day) < (value.month, value.day))
        
        if idade < 16:
            raise serializers.ValidationError(
                'Estagiário deve ter pelo menos 16 anos.'
            )
        if idade > 100:
            raise serializers.ValidationError(
                'Data de nascimento inválida.'
            )
        return value


class ConvenioSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Convênio"""
    
    total_estagios = serializers.SerializerMethodField()
    estagios_ativos = serializers.SerializerMethodField()
    
    class Meta:
        model = Convenio
        fields = [
            'id', 'nome_empresa', 'cnpj', 'endereco', 'telefone',
            'responsavel', 'email_responsavel', 'ativo',
            'total_estagios', 'estagios_ativos',
            'data_cadastro', 'data_atualizacao'
        ]
        read_only_fields = ['data_cadastro', 'data_atualizacao']
    
    def get_total_estagios(self, obj):
        """Retorna o total de estágios da empresa"""
        return obj.estagios.count()
    
    def get_estagios_ativos(self, obj):
        """Retorna o total de estágios ativos da empresa"""
        return obj.estagios.filter(status='EM_ANDAMENTO').count()
    
    def validate_cnpj(self, value):
        """Validação personalizada para CNPJ"""
        if not re.match(r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$', value):
            raise serializers.ValidationError(
                'CNPJ deve estar no formato: 00.000.000/0000-00'
            )
        return value
    
    def validate_telefone(self, value):
        """Validação personalizada para telefone"""
        if not re.match(r'^\(\d{2}\) \d{4,5}-\d{4}$', value):
            raise serializers.ValidationError(
                'Telefone deve estar no formato: (00) 00000-0000'
            )
        return value


class EstagioSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Estágio"""
    
    estagiario_nome = serializers.CharField(source='estagiario.nome', read_only=True)
    convenio_nome = serializers.CharField(source='convenio.nome_empresa', read_only=True)
    duracao_dias = serializers.ReadOnlyField()
    dias_restantes = serializers.ReadOnlyField()
    total_documentos = serializers.SerializerMethodField()
    
    class Meta:
        model = Estagio
        fields = [
            'id', 'estagiario', 'estagiario_nome', 'convenio', 'convenio_nome',
            'supervisor', 'supervisor_email', 'carga_horaria',
            'data_inicio', 'data_fim', 'status', 'observacoes',
            'duracao_dias', 'dias_restantes', 'total_documentos',
            'data_cadastro', 'data_atualizacao'
        ]
        read_only_fields = ['data_cadastro', 'data_atualizacao']
    
    def get_total_documentos(self, obj):
        """Retorna o total de documentos do estágio"""
        return obj.documentos.count()
    
    def validate(self, data):
        """Validação personalizada para o estágio"""
        data_inicio = data.get('data_inicio')
        data_fim = data.get('data_fim')
        
        if data_inicio and data_fim:
            if data_inicio >= data_fim:
                raise serializers.ValidationError(
                    'Data de início deve ser anterior à data de fim.'
                )
            
            # Verificar se o período não é muito longo (máximo 2 anos)
            duracao = (data_fim - data_inicio).days
            if duracao > 730:  # 2 anos
                raise serializers.ValidationError(
                    'Duração do estágio não pode exceder 2 anos.'
                )
            
            if duracao < 30:  # Mínimo 30 dias
                raise serializers.ValidationError(
                    'Duração do estágio deve ser de pelo menos 30 dias.'
                )
        
        # Verificar se o estagiário já tem um estágio ativo no mesmo período
        estagiario = data.get('estagiario')
        if estagiario and data_inicio and data_fim:
            estagios_conflito = Estagio.objects.filter(
                estagiario=estagiario,
                status='EM_ANDAMENTO'
            ).exclude(id=self.instance.id if self.instance else None)
            
            for estagio in estagios_conflito:
                if (data_inicio <= estagio.data_fim and data_fim >= estagio.data_inicio):
                    raise serializers.ValidationError(
                        f'Estagiário já possui estágio ativo no período: '
                        f'{estagio.data_inicio} a {estagio.data_fim}'
                    )
        
        return data
    
    def validate_carga_horaria(self, value):
        """Validação para carga horária"""
        if value < 20:
            raise serializers.ValidationError(
                'Carga horária deve ser de pelo menos 20 horas.'
            )
        if value > 40:
            raise serializers.ValidationError(
                'Carga horária não pode exceder 40 horas semanais.'
            )
        return value


class DocumentoSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Documento"""
    
    estagio_info = serializers.SerializerMethodField()
    usuario_upload_nome = serializers.CharField(
        source='usuario_upload.username', 
        read_only=True
    )
    arquivo_url = serializers.SerializerMethodField()
    arquivo_nome = serializers.SerializerMethodField()
    
    class Meta:
        model = Documento
        fields = [
            'id', 'estagio', 'estagio_info', 'tipo_documento', 
            'arquivo', 'arquivo_url', 'arquivo_nome', 'descricao',
            'data_upload', 'usuario_upload', 'usuario_upload_nome'
        ]
        read_only_fields = ['data_upload', 'usuario_upload']
    
    def get_estagio_info(self, obj):
        """Retorna informações resumidas do estágio"""
        return {
            'id': obj.estagio.id,
            'estagiario': obj.estagio.estagiario.nome,
            'empresa': obj.estagio.convenio.nome_empresa
        }
    
    def get_arquivo_url(self, obj):
        """Retorna a URL do arquivo"""
        if obj.arquivo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.arquivo.url)
            return obj.arquivo.url
        return None
    
    def get_arquivo_nome(self, obj):
        """Retorna o nome do arquivo"""
        if obj.arquivo:
            return obj.arquivo.name.split('/')[-1]
        return None
    
    def validate_arquivo(self, value):
        """Validação para o arquivo"""
        if value:
            # Verificar tamanho do arquivo (máximo 10MB)
            if value.size > 10 * 1024 * 1024:
                raise serializers.ValidationError(
                    'Arquivo muito grande. Tamanho máximo: 10MB.'
                )
            
            # Verificar extensão do arquivo
            extensoes_permitidas = [
                '.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png', '.txt'
            ]
            nome_arquivo = value.name.lower()
            if not any(nome_arquivo.endswith(ext) for ext in extensoes_permitidas):
                raise serializers.ValidationError(
                    f'Tipo de arquivo não permitido. '
                    f'Extensões permitidas: {", ".join(extensoes_permitidas)}'
                )
        
        return value


class NotificacaoSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Notificação"""
    
    estagiario_nome = serializers.CharField(source='estagiario.nome', read_only=True)
    tempo_desde_envio = serializers.SerializerMethodField()
    
    class Meta:
        model = Notificacao
        fields = [
            'id', 'estagiario', 'estagiario_nome', 'titulo', 'mensagem',
            'tipo', 'lida', 'data_envio', 'data_leitura', 'tempo_desde_envio'
        ]
        read_only_fields = ['data_envio', 'data_leitura']
    
    def get_tempo_desde_envio(self, obj):
        """Retorna o tempo desde o envio da notificação"""
        agora = timezone.now()
        diferenca = agora - obj.data_envio
        
        if diferenca.days > 0:
            return f'{diferenca.days} dia(s) atrás'
        elif diferenca.seconds > 3600:
            horas = diferenca.seconds // 3600
            return f'{horas} hora(s) atrás'
        elif diferenca.seconds > 60:
            minutos = diferenca.seconds // 60
            return f'{minutos} minuto(s) atrás'
        else:
            return 'Agora mesmo'


class NotificacaoCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de notificações"""
    
    class Meta:
        model = Notificacao
        fields = ['estagiario', 'titulo', 'mensagem', 'tipo']
    
    def validate_titulo(self, value):
        """Validação para o título"""
        if len(value.strip()) < 5:
            raise serializers.ValidationError(
                'Título deve ter pelo menos 5 caracteres.'
            )
        return value.strip()
    
    def validate_mensagem(self, value):
        """Validação para a mensagem"""
        if len(value.strip()) < 10:
            raise serializers.ValidationError(
                'Mensagem deve ter pelo menos 10 caracteres.'
            )
        return value.strip()


class EstatisticasSistemaSerializer(serializers.ModelSerializer):
    """Serializer para as estatísticas do sistema"""
    
    percentual_estagiarios_ativos = serializers.SerializerMethodField()
    percentual_estagios_em_andamento = serializers.SerializerMethodField()
    percentual_convenios_ativos = serializers.SerializerMethodField()
    
    class Meta:
        model = EstatisticasSistema
        fields = [
            'data_calculo', 'total_estagiarios', 'estagiarios_ativos',
            'total_estagios', 'estagios_em_andamento', 'total_convenios',
            'convenios_ativos', 'total_documentos', 'notificacoes_nao_lidas',
            'percentual_estagiarios_ativos', 'percentual_estagios_em_andamento',
            'percentual_convenios_ativos'
        ]
    
    def get_percentual_estagiarios_ativos(self, obj):
        """Calcula o percentual de estagiários ativos"""
        if obj.total_estagiarios > 0:
            return round((obj.estagiarios_ativos / obj.total_estagiarios) * 100, 2)
        return 0
    
    def get_percentual_estagios_em_andamento(self, obj):
        """Calcula o percentual de estágios em andamento"""
        if obj.total_estagios > 0:
            return round((obj.estagios_em_andamento / obj.total_estagios) * 100, 2)
        return 0
    
    def get_percentual_convenios_ativos(self, obj):
        """Calcula o percentual de convênios ativos"""
        if obj.total_convenios > 0:
            return round((obj.convenios_ativos / obj.total_convenios) * 100, 2)
        return 0


class UserSerializer(serializers.ModelSerializer):
    """Serializer para usuários (para informações básicas)"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff']
        read_only_fields = ['id', 'is_staff']


# Serializers para relatórios e estatísticas específicas
class RelatorioEstagiarioSerializer(serializers.Serializer):
    """Serializer para relatório de estagiários"""
    
    periodo_inicio = serializers.DateField()
    periodo_fim = serializers.DateField()
    status = serializers.ChoiceField(
        choices=[('TODOS', 'Todos')] + Estagiario.STATUS_CHOICES,
        default='TODOS'
    )
    curso = serializers.CharField(required=False, allow_blank=True)
    
    def validate(self, data):
        """Validação do período"""
        if data['periodo_inicio'] >= data['periodo_fim']:
            raise serializers.ValidationError(
                'Data de início deve ser anterior à data de fim.'
            )
        return data


class RelatorioEstagioSerializer(serializers.Serializer):
    """Serializer para relatório de estágios"""
    
    periodo_inicio = serializers.DateField()
    periodo_fim = serializers.DateField()
    status = serializers.ChoiceField(
        choices=[('TODOS', 'Todos')] + Estagio.STATUS_CHOICES,
        default='TODOS'
    )
    convenio = serializers.IntegerField(required=False)
    
    def validate(self, data):
        """Validação do período"""
        if data['periodo_inicio'] >= data['periodo_fim']:
            raise serializers.ValidationError(
                'Data de início deve ser anterior à data de fim.'
            )
        return data


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Notification"""
    
    class Meta:
        model = Notification
        fields = ['id', 'message', 'due_date', 'read', 'created_at']

