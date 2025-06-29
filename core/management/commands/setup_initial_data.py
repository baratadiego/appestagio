"""
Comando para configurar dados iniciais do sistema
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, timedelta
from core.models import (
    Estagiario, Convenio, Estagio, Documento, 
    Notificacao, EstatisticasSistema
)


class Command(BaseCommand):
    help = 'Configura dados iniciais para o sistema de estágios'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--create-superuser',
            action='store_true',
            help='Cria um superusuário admin/admin123',
        )
        parser.add_argument(
            '--create-sample-data',
            action='store_true',
            help='Cria dados de exemplo',
        )
    
    def handle(self, *args, **options):
        if options['create_superuser']:
            self.create_superuser()
        
        if options['create_sample_data']:
            self.create_sample_data()
        
        # Sempre calcular estatísticas no final
        self.calculate_statistics()
    
    def create_superuser(self):
        """Cria um superusuário padrão"""
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@estagios.com',
                password='admin123'
            )
            self.stdout.write(
                self.style.SUCCESS('Superusuário criado: admin/admin123')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Superusuário "admin" já existe')
            )
    
    def create_sample_data(self):
        """Cria dados de exemplo"""
        self.stdout.write('Criando dados de exemplo...')
        
        # Criar convênios
        convenios_data = [
            {
                'nome_empresa': 'TechCorp Soluções',
                'cnpj': '12.345.678/0001-90',
                'endereco': 'Rua das Tecnologias, 123 - Centro',
                'telefone': '(11) 3456-7890',
                'responsavel': 'João Silva',
                'email_responsavel': 'joao.silva@techcorp.com'
            },
            {
                'nome_empresa': 'Inovação Digital Ltda',
                'cnpj': '98.765.432/0001-10',
                'endereco': 'Av. Inovação, 456 - Tecnópolis',
                'telefone': '(11) 9876-5432',
                'responsavel': 'Maria Santos',
                'email_responsavel': 'maria.santos@inovacao.com'
            },
            {
                'nome_empresa': 'StartUp Criativa',
                'cnpj': '11.222.333/0001-44',
                'endereco': 'Rua Criativa, 789 - Vila Tech',
                'telefone': '(11) 1122-3344',
                'responsavel': 'Pedro Costa',
                'email_responsavel': 'pedro.costa@startup.com'
            }
        ]
        
        convenios = []
        for convenio_data in convenios_data:
            convenio, created = Convenio.objects.get_or_create(
                cnpj=convenio_data['cnpj'],
                defaults=convenio_data
            )
            convenios.append(convenio)
            if created:
                self.stdout.write(f'Convênio criado: {convenio.nome_empresa}')
        
        # Criar estagiários
        estagiarios_data = [
            {
                'nome': 'Ana Carolina Silva',
                'email': 'ana.silva@email.com',
                'telefone': '(11) 99999-1111',
                'curso': 'Ciência da Computação',
                'periodo': '7º Semestre',
                'cpf': '123.456.789-01',
                'data_nascimento': date(2000, 5, 15)
            },
            {
                'nome': 'Bruno Santos Oliveira',
                'email': 'bruno.oliveira@email.com',
                'telefone': '(11) 99999-2222',
                'curso': 'Sistemas de Informação',
                'periodo': '6º Semestre',
                'cpf': '987.654.321-02',
                'data_nascimento': date(1999, 8, 22)
            },
            {
                'nome': 'Carla Fernanda Costa',
                'email': 'carla.costa@email.com',
                'telefone': '(11) 99999-3333',
                'curso': 'Engenharia de Software',
                'periodo': '8º Semestre',
                'cpf': '456.789.123-03',
                'data_nascimento': date(2001, 2, 10)
            },
            {
                'nome': 'Daniel Rodrigues Lima',
                'email': 'daniel.lima@email.com',
                'telefone': '(11) 99999-4444',
                'curso': 'Análise e Desenvolvimento de Sistemas',
                'periodo': '4º Semestre',
                'cpf': '789.123.456-04',
                'data_nascimento': date(2002, 11, 5)
            }
        ]
        
        estagiarios = []
        for estagiario_data in estagiarios_data:
            estagiario, created = Estagiario.objects.get_or_create(
                cpf=estagiario_data['cpf'],
                defaults=estagiario_data
            )
            estagiarios.append(estagiario)
            if created:
                self.stdout.write(f'Estagiário criado: {estagiario.nome}')
        
        # Criar estágios
        hoje = date.today()
        estagios_data = [
            {
                'estagiario': estagiarios[0],
                'convenio': convenios[0],
                'supervisor': 'Carlos Mendes',
                'supervisor_email': 'carlos.mendes@techcorp.com',
                'carga_horaria': 30,
                'data_inicio': hoje - timedelta(days=60),
                'data_fim': hoje + timedelta(days=120),
                'status': 'EM_ANDAMENTO',
                'observacoes': 'Estágio em desenvolvimento web'
            },
            {
                'estagiario': estagiarios[1],
                'convenio': convenios[1],
                'supervisor': 'Fernanda Alves',
                'supervisor_email': 'fernanda.alves@inovacao.com',
                'carga_horaria': 25,
                'data_inicio': hoje - timedelta(days=30),
                'data_fim': hoje + timedelta(days=150),
                'status': 'EM_ANDAMENTO',
                'observacoes': 'Estágio em análise de sistemas'
            },
            {
                'estagiario': estagiarios[2],
                'convenio': convenios[2],
                'supervisor': 'Roberto Ferreira',
                'supervisor_email': 'roberto.ferreira@startup.com',
                'carga_horaria': 35,
                'data_inicio': hoje - timedelta(days=180),
                'data_fim': hoje - timedelta(days=30),
                'status': 'FINALIZADO',
                'observacoes': 'Estágio finalizado com sucesso'
            }
        ]
        
        estagios = []
        for estagio_data in estagios_data:
            estagio, created = Estagio.objects.get_or_create(
                estagiario=estagio_data['estagiario'],
                convenio=estagio_data['convenio'],
                data_inicio=estagio_data['data_inicio'],
                defaults=estagio_data
            )
            estagios.append(estagio)
            if created:
                self.stdout.write(
                    f'Estágio criado: {estagio.estagiario.nome} - {estagio.convenio.nome_empresa}'
                )
        
        # Criar notificações
        notificacoes_data = [
            {
                'estagiario': estagiarios[0],
                'titulo': 'Bem-vindo ao sistema!',
                'mensagem': 'Seja bem-vindo ao sistema de gerenciamento de estágios.',
                'tipo': 'INFO'
            },
            {
                'estagiario': estagiarios[1],
                'titulo': 'Documentos pendentes',
                'mensagem': 'Você possui documentos pendentes de envio.',
                'tipo': 'ALERTA'
            },
            {
                'estagiario': estagiarios[0],
                'titulo': 'Estágio próximo do fim',
                'mensagem': 'Seu estágio está próximo do fim. Prepare a documentação final.',
                'tipo': 'URGENTE'
            }
        ]
        
        for notificacao_data in notificacoes_data:
            notificacao, created = Notificacao.objects.get_or_create(
                estagiario=notificacao_data['estagiario'],
                titulo=notificacao_data['titulo'],
                defaults=notificacao_data
            )
            if created:
                self.stdout.write(
                    f'Notificação criada: {notificacao.titulo}'
                )
        
        self.stdout.write(
            self.style.SUCCESS('Dados de exemplo criados com sucesso!')
        )
    
    def calculate_statistics(self):
        """Calcula as estatísticas do sistema"""
        stats = EstatisticasSistema.calcular_estatisticas()
        self.stdout.write(
            self.style.SUCCESS('Estatísticas calculadas e atualizadas!')
        )

