# Sistema de Gerenciamento de Estágios Supervisionados

Um sistema web completo desenvolvido em Django + Django REST Framework para gerenciar estágios supervisionados, com autenticação JWT, banco PostgreSQL e containerização Docker.

## 📋 Índice

- [Características](#características)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação e Configuração](#instalação-e-configuração)
- [Uso com Docker](#uso-com-docker)
- [API Endpoints](#api-endpoints)
- [Autenticação](#autenticação)
- [Modelos de Dados](#modelos-de-dados)
- [Permissões](#permissões)
- [Administração](#administração)
- [Desenvolvimento](#desenvolvimento)
- [Produção](#produção)
- [Contribuição](#contribuição)

## 🚀 Características

### Funcionalidades Principais

- **Cadastro de Estagiários**: Gerenciamento completo de dados pessoais e acadêmicos
- **Registro de Convênios**: Controle de empresas parceiras e responsáveis
- **Acompanhamento de Estágios**: Monitoramento de períodos, supervisores e status
- **Documentação Digital**: Upload e download de documentos com controle de versão
- **Sistema de Notificações**: Alertas automáticos e comunicação interna
- **Painel Administrativo**: Estatísticas e relatórios em tempo real
- **API RESTful**: Endpoints seguros para integração com outras aplicações

### Características Técnicas

- **Autenticação JWT**: Sistema seguro de autenticação com tokens
- **Permissões Granulares**: Controle de acesso baseado em roles
- **Validações Robustas**: Validação de dados em múltiplas camadas
- **Containerização**: Deploy simplificado com Docker
- **Banco PostgreSQL**: Banco de dados robusto e escalável
- **Interface Admin**: Painel administrativo Django customizado

## 🛠 Tecnologias Utilizadas

### Backend
- **Django 4.2.7**: Framework web Python
- **Django REST Framework 3.14.0**: API REST
- **Django REST Framework SimpleJWT 5.3.0**: Autenticação JWT
- **PostgreSQL**: Banco de dados principal
- **Redis**: Cache e sessões (opcional)

### Infraestrutura
- **Docker & Docker Compose**: Containerização
- **Nginx**: Proxy reverso e servidor web
- **Gunicorn**: Servidor WSGI para produção
- **pgAdmin**: Interface de administração do PostgreSQL

### Bibliotecas Auxiliares
- **django-cors-headers**: Configuração CORS
- **Pillow**: Processamento de imagens
- **python-decouple**: Gerenciamento de configurações
- **whitenoise**: Servir arquivos estáticos
- **django-filter**: Filtros avançados para API

## 📁 Estrutura do Projeto

```
estagios_system/
├── estagios/                 # Configurações principais do Django
│   ├── __init__.py
│   ├── settings.py          # Configurações do projeto
│   ├── urls.py              # URLs principais
│   ├── wsgi.py              # Configuração WSGI
│   └── asgi.py              # Configuração ASGI
├── core/                    # App principal do sistema
│   ├── migrations/          # Migrações do banco de dados
│   ├── management/          # Comandos personalizados
│   │   └── commands/
│   │       └── setup_initial_data.py
│   ├── __init__.py
│   ├── admin.py            # Configuração do admin
│   ├── apps.py             # Configuração do app
│   ├── models.py           # Modelos de dados
│   ├── serializers.py      # Serializers do DRF
│   ├── views.py            # Views e ViewSets
│   ├── urls.py             # URLs do app
│   ├── permissions.py      # Permissões customizadas
│   └── tests.py            # Testes unitários
├── docker/                 # Configurações Docker
│   ├── postgres/
│   │   └── init.sql
│   ├── pgadmin/
│   │   └── servers.json
│   └── nginx/
│       ├── nginx.conf
│       ├── default.conf
│       └── ssl/
├── media/                  # Arquivos de mídia (uploads)
├── static/                 # Arquivos estáticos (desenvolvimento)
├── staticfiles/           # Arquivos estáticos (produção)
├── logs/                  # Logs da aplicação
├── Dockerfile             # Configuração Docker da aplicação
├── docker-compose.yml     # Orquestração dos containers
├── docker-entrypoint.sh   # Script de entrada do container
├── requirements.txt       # Dependências Python
├── .env                   # Variáveis de ambiente
├── .dockerignore         # Arquivos ignorados no build
└── README.md             # Esta documentação
```


## ⚙️ Instalação e Configuração

### Pré-requisitos

- Python 3.11+
- PostgreSQL 12+ (ou Docker)
- Git

### Instalação Local (Desenvolvimento)

1. **Clone o repositório**
```bash
git clone <url-do-repositorio>
cd estagios_system
```

2. **Crie e ative um ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. **Configure o banco de dados**
```bash
# Para desenvolvimento com SQLite (padrão)
python manage.py migrate

# Para PostgreSQL, configure DATABASE_URL no .env
export DATABASE_URL="postgresql://user:password@localhost:5432/estagios_db"
python manage.py migrate
```

6. **Crie dados iniciais**
```bash
python manage.py setup_initial_data --create-superuser --create-sample-data
```

7. **Execute o servidor de desenvolvimento**
```bash
python manage.py runserver
```

A aplicação estará disponível em `http://localhost:8000`

### Configuração das Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# Configurações Django
DEBUG=True
SECRET_KEY=sua-chave-secreta-aqui

# Banco de dados (opcional para desenvolvimento)
DATABASE_URL=postgresql://estagios_user:estagios_pass@localhost:5432/estagios_db

# PostgreSQL (para Docker)
POSTGRES_DB=estagios_db
POSTGRES_USER=estagios_user
POSTGRES_PASSWORD=estagios_pass
POSTGRES_HOST=db
POSTGRES_PORT=5432

# pgAdmin
PGADMIN_DEFAULT_EMAIL=admin@estagios.com
PGADMIN_DEFAULT_PASSWORD=admin123

# Configurações adicionais
SETUP_INITIAL_DATA=true
```

## 🐳 Uso com Docker

### Desenvolvimento com Docker

1. **Clone o repositório**
```bash
git clone <url-do-repositorio>
cd estagios_system
```

2. **Configure as variáveis de ambiente**
```bash
cp .env.example .env
# Edite conforme necessário
```

3. **Execute com Docker Compose**
```bash
# Construir e executar todos os serviços
docker-compose up --build

# Executar em background
docker-compose up -d

# Ver logs
docker-compose logs -f web
```

4. **Acesse os serviços**
- **Aplicação Django**: http://localhost:8000
- **Admin Django**: http://localhost:8000/admin (admin/admin123)
- **pgAdmin**: http://localhost:5050 (admin@estagios.com/admin123)
- **API**: http://localhost:8000/api/v1/

### Comandos Úteis do Docker

```bash
# Parar todos os serviços
docker-compose down

# Parar e remover volumes (CUIDADO: apaga dados do banco)
docker-compose down -v

# Reconstruir apenas a aplicação
docker-compose build web

# Executar comandos Django no container
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic

# Ver logs de um serviço específico
docker-compose logs -f db
docker-compose logs -f web

# Acessar shell do container
docker-compose exec web bash
docker-compose exec db psql -U estagios_user -d estagios_db
```

### Produção com Docker

Para produção, use o perfil específico que inclui Nginx:

```bash
# Executar com Nginx (produção)
docker-compose --profile production up -d

# Configurar SSL (edite os certificados em docker/nginx/ssl/)
# Ajustar configurações de segurança no .env
```

## 🔌 API Endpoints

### Autenticação

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/auth/login/` | Obter token JWT |
| POST | `/api/auth/refresh/` | Renovar token JWT |
| POST | `/api/auth/verify/` | Verificar token JWT |

**Exemplo de Login:**
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### Estagiários

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/v1/estagiarios/` | Listar estagiários |
| POST | `/api/v1/estagiarios/` | Criar estagiário |
| GET | `/api/v1/estagiarios/{id}/` | Detalhar estagiário |
| PUT | `/api/v1/estagiarios/{id}/` | Atualizar estagiário |
| DELETE | `/api/v1/estagiarios/{id}/` | Deletar estagiário |
| GET | `/api/v1/estagiarios/ativos/` | Listar apenas ativos |
| GET | `/api/v1/estagiarios/{id}/estagios/` | Estágios do estagiário |
| GET | `/api/v1/estagiarios/{id}/notificacoes/` | Notificações do estagiário |

### Convênios

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/v1/convenios/` | Listar convênios |
| POST | `/api/v1/convenios/` | Criar convênio |
| GET | `/api/v1/convenios/{id}/` | Detalhar convênio |
| PUT | `/api/v1/convenios/{id}/` | Atualizar convênio |
| DELETE | `/api/v1/convenios/{id}/` | Deletar convênio |
| GET | `/api/v1/convenios/ativos/` | Listar apenas ativos |
| POST | `/api/v1/convenios/{id}/ativar/` | Ativar convênio |
| POST | `/api/v1/convenios/{id}/desativar/` | Desativar convênio |

### Estágios

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/v1/estagios/` | Listar estágios |
| POST | `/api/v1/estagios/` | Criar estágio |
| GET | `/api/v1/estagios/{id}/` | Detalhar estágio |
| PUT | `/api/v1/estagios/{id}/` | Atualizar estágio |
| DELETE | `/api/v1/estagios/{id}/` | Deletar estágio |
| GET | `/api/v1/estagios/em_andamento/` | Estágios em andamento |
| GET | `/api/v1/estagios/finalizados/` | Estágios finalizados |
| GET | `/api/v1/estagios/vencendo/` | Estágios vencendo em 30 dias |
| POST | `/api/v1/estagios/{id}/finalizar/` | Finalizar estágio |
| POST | `/api/v1/estagios/{id}/cancelar/` | Cancelar estágio |

### Documentos

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/v1/documentos/` | Listar documentos |
| POST | `/api/v1/documentos/` | Upload de documento |
| GET | `/api/v1/documentos/{id}/` | Detalhar documento |
| DELETE | `/api/v1/documentos/{id}/` | Deletar documento |
| GET | `/api/v1/documentos/{id}/download/` | Download do arquivo |
| GET | `/api/v1/documentos/por_tipo/?tipo=TERMO_COMPROMISSO` | Filtrar por tipo |

### Notificações

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/v1/notificacoes/` | Listar notificações |
| POST | `/api/v1/notificacoes/` | Criar notificação |
| GET | `/api/v1/notificacoes/{id}/` | Detalhar notificação |
| DELETE | `/api/v1/notificacoes/{id}/` | Deletar notificação |
| GET | `/api/v1/notificacoes/nao_lidas/` | Notificações não lidas |
| POST | `/api/v1/notificacoes/{id}/marcar_lida/` | Marcar como lida |
| POST | `/api/v1/notificacoes/marcar_todas_lidas/` | Marcar todas como lidas |

### Estatísticas e Relatórios

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/v1/estatisticas/` | Estatísticas do sistema |
| POST | `/api/v1/estatisticas/` | Atualizar estatísticas |
| POST | `/api/v1/relatorios/estagiarios/` | Relatório de estagiários |
| POST | `/api/v1/relatorios/estagios/` | Relatório de estágios |

### Filtros e Busca

Todos os endpoints de listagem suportam:

- **Busca**: `?search=termo`
- **Filtros**: `?campo=valor`
- **Ordenação**: `?ordering=campo` ou `?ordering=-campo`
- **Paginação**: `?page=1&page_size=20`

**Exemplos:**
```bash
# Buscar estagiários por nome
GET /api/v1/estagiarios/?search=João

# Filtrar estagiários ativos do curso de Computação
GET /api/v1/estagiarios/?status=ATIVO&curso=Ciência da Computação

# Ordenar estágios por data de início (mais recentes primeiro)
GET /api/v1/estagios/?ordering=-data_inicio

# Paginação personalizada
GET /api/v1/estagiarios/?page=2&page_size=10
```


## 🔐 Autenticação

O sistema utiliza **JWT (JSON Web Tokens)** para autenticação, implementado com `djangorestframework-simplejwt`.

### Configuração JWT

- **Access Token**: Válido por 1 hora
- **Refresh Token**: Válido por 7 dias
- **Rotação automática**: Tokens são renovados automaticamente
- **Blacklist**: Tokens invalidados são mantidos em blacklist

### Fluxo de Autenticação

1. **Login**: Envie credenciais para `/api/auth/login/`
2. **Receba tokens**: Access token e refresh token
3. **Use access token**: Inclua no header `Authorization: Bearer <token>`
4. **Renove quando necessário**: Use refresh token em `/api/auth/refresh/`

### Exemplo de Uso

```python
import requests

# 1. Login
response = requests.post('http://localhost:8000/api/auth/login/', {
    'username': 'admin',
    'password': 'admin123'
})
tokens = response.json()

# 2. Usar token nas requisições
headers = {
    'Authorization': f'Bearer {tokens["access"]}'
}

# 3. Fazer requisições autenticadas
response = requests.get(
    'http://localhost:8000/api/v1/estagiarios/',
    headers=headers
)

# 4. Renovar token quando necessário
refresh_response = requests.post(
    'http://localhost:8000/api/auth/refresh/',
    {'refresh': tokens['refresh']}
)
new_access_token = refresh_response.json()['access']
```

### Headers de Autenticação

```bash
# Incluir em todas as requisições autenticadas
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

## 📊 Modelos de Dados

### Estagiário

Armazena informações dos estudantes em estágio.

```python
class Estagiario(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15)  # (00) 00000-0000
    curso = models.CharField(max_length=100)
    periodo = models.CharField(max_length=20)
    cpf = models.CharField(max_length=14, unique=True)  # 000.000.000-00
    data_nascimento = models.DateField()
    status = models.CharField(choices=[('ATIVO', 'Ativo'), ('INATIVO', 'Inativo')])
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
```

**Validações:**
- CPF no formato 000.000.000-00
- Telefone no formato (00) 00000-0000
- Idade mínima de 16 anos
- Email único no sistema

### Convênio

Representa empresas parceiras que oferecem estágios.

```python
class Convenio(models.Model):
    nome_empresa = models.CharField(max_length=200)
    cnpj = models.CharField(max_length=18, unique=True)  # 00.000.000/0000-00
    endereco = models.TextField()
    telefone = models.CharField(max_length=15)
    responsavel = models.CharField(max_length=200)
    email_responsavel = models.EmailField(blank=True, null=True)
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
```

**Validações:**
- CNPJ no formato 00.000.000/0000-00
- Telefone no formato (00) 00000-0000
- Nome da empresa obrigatório

### Estágio

Relaciona estagiários com convênios, controlando o período de estágio.

```python
class Estagio(models.Model):
    estagiario = models.ForeignKey(Estagiario, on_delete=models.CASCADE)
    convenio = models.ForeignKey(Convenio, on_delete=models.CASCADE)
    supervisor = models.CharField(max_length=200)
    supervisor_email = models.EmailField(blank=True, null=True)
    carga_horaria = models.PositiveIntegerField()  # horas semanais
    data_inicio = models.DateField()
    data_fim = models.DateField()
    status = models.CharField(choices=[
        ('EM_ANDAMENTO', 'Em Andamento'),
        ('FINALIZADO', 'Finalizado'),
        ('CANCELADO', 'Cancelado'),
        ('SUSPENSO', 'Suspenso')
    ])
    observacoes = models.TextField(blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
```

**Validações:**
- Data de início anterior à data de fim
- Duração mínima de 30 dias
- Duração máxima de 2 anos
- Carga horária entre 20 e 40 horas semanais
- Não permitir sobreposição de estágios para o mesmo estagiário

### Documento

Armazena arquivos relacionados aos estágios.

```python
class Documento(models.Model):
    estagio = models.ForeignKey(Estagio, on_delete=models.CASCADE)
    tipo_documento = models.CharField(choices=[
        ('TERMO_COMPROMISSO', 'Termo de Compromisso'),
        ('PLANO_ESTAGIO', 'Plano de Estágio'),
        ('RELATORIO', 'Relatório'),
        ('AVALIACAO', 'Avaliação'),
        ('OUTROS', 'Outros')
    ])
    arquivo = models.FileField(upload_to='documentos/')
    descricao = models.CharField(max_length=200, blank=True)
    data_upload = models.DateTimeField(auto_now_add=True)
    usuario_upload = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
```

**Validações:**
- Tamanho máximo de 10MB
- Extensões permitidas: .pdf, .doc, .docx, .jpg, .jpeg, .png, .txt
- Descrição opcional

### Notificação

Sistema de mensagens e alertas para estagiários.

```python
class Notificacao(models.Model):
    estagiario = models.ForeignKey(Estagiario, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    mensagem = models.TextField()
    tipo = models.CharField(choices=[
        ('INFO', 'Informação'),
        ('ALERTA', 'Alerta'),
        ('URGENTE', 'Urgente')
    ])
    lida = models.BooleanField(default=False)
    data_envio = models.DateTimeField(auto_now_add=True)
    data_leitura = models.DateTimeField(null=True, blank=True)
```

**Validações:**
- Título mínimo de 5 caracteres
- Mensagem mínima de 10 caracteres
- Data de leitura automática ao marcar como lida

### Estatísticas do Sistema

Cache de estatísticas para o painel administrativo.

```python
class EstatisticasSistema(models.Model):
    data_calculo = models.DateTimeField(auto_now=True)
    total_estagiarios = models.PositiveIntegerField(default=0)
    estagiarios_ativos = models.PositiveIntegerField(default=0)
    total_estagios = models.PositiveIntegerField(default=0)
    estagios_em_andamento = models.PositiveIntegerField(default=0)
    total_convenios = models.PositiveIntegerField(default=0)
    convenios_ativos = models.PositiveIntegerField(default=0)
    total_documentos = models.PositiveIntegerField(default=0)
    notificacoes_nao_lidas = models.PositiveIntegerField(default=0)
```

## 🔒 Permissões

O sistema implementa um controle de acesso granular com permissões personalizadas.

### Tipos de Usuários

1. **Administradores** (`is_staff=True`):
   - Acesso completo a todos os recursos
   - Podem criar, editar e deletar qualquer registro
   - Acesso ao painel administrativo
   - Podem gerar relatórios e ver estatísticas

2. **Usuários Comuns** (`is_staff=False`):
   - Acesso limitado baseado em relacionamentos
   - Podem ver apenas dados relacionados a eles
   - Não podem deletar registros importantes

### Permissões Implementadas

#### `IsAdminOrReadOnly`
- **Administradores**: CRUD completo
- **Usuários comuns**: Apenas leitura

#### `IsEstagiarioOwnerOrAdmin`
- **Administradores**: Acesso total
- **Estagiários**: Apenas seus próprios dados

#### `CanManageDocuments`
- **Administradores**: Gerenciar todos os documentos
- **Estagiários**: Upload e download de documentos dos próprios estágios
- **Supervisores**: Acesso aos documentos dos estágios supervisionados

#### `CanManageNotifications`
- **Administradores**: Criar e gerenciar todas as notificações
- **Estagiários**: Ver e marcar como lidas apenas suas notificações

#### `CanAccessStatistics`
- **Apenas administradores**: Acesso às estatísticas do sistema

#### `CanGenerateReports`
- **Apenas administradores**: Geração de relatórios

### Aplicação das Permissões

```python
# Exemplo de uso nas views
class EstagiarioViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]

class DocumentoViewSet(viewsets.ModelViewSet):
    permission_classes = [CanManageDocuments]

class EstatisticasView(APIView):
    permission_classes = [CanAccessStatistics]
```

### Verificação de Permissões

As permissões são verificadas automaticamente pelo Django REST Framework:

1. **Nível de View**: Verificação geral de acesso
2. **Nível de Objeto**: Verificação específica por registro
3. **Nível de Campo**: Controle de campos sensíveis

### Exemplos de Controle de Acesso

```python
# Estagiário só vê seus próprios estágios
def get_queryset(self):
    if self.request.user.is_staff:
        return Estagio.objects.all()
    else:
        return Estagio.objects.filter(
            estagiario__email=self.request.user.email
        )

# Supervisor vê estágios que supervisiona
def get_queryset(self):
    if self.request.user.is_staff:
        return Estagio.objects.all()
    else:
        return Estagio.objects.filter(
            supervisor_email=self.request.user.email
        )
```


## 🎛 Administração

### Painel Administrativo Django

Acesse em `http://localhost:8000/admin/` com as credenciais de administrador.

#### Funcionalidades do Admin

1. **Gestão de Usuários**: Criar e gerenciar contas de usuário
2. **CRUD Completo**: Todas as entidades podem ser gerenciadas
3. **Filtros Avançados**: Busca e filtros em todas as listagens
4. **Ações em Lote**: Operações em múltiplos registros
5. **Estatísticas**: Contadores e métricas em tempo real
6. **Logs de Auditoria**: Histórico de alterações

#### Customizações Implementadas

- **Interface personalizada** com títulos e descrições em português
- **Filtros inteligentes** por status, datas e relacionamentos
- **Ações customizadas** como ativar/desativar em lote
- **Campos calculados** como idade, duração de estágios
- **Links relacionados** entre entidades
- **Validações em tempo real** nos formulários

### Comandos de Gerenciamento

#### Setup de Dados Iniciais

```bash
# Criar superusuário e dados de exemplo
python manage.py setup_initial_data --create-superuser --create-sample-data

# Apenas superusuário
python manage.py setup_initial_data --create-superuser

# Apenas dados de exemplo
python manage.py setup_initial_data --create-sample-data
```

#### Outros Comandos Úteis

```bash
# Criar superusuário interativo
python manage.py createsuperuser

# Coletar arquivos estáticos
python manage.py collectstatic

# Limpar sessões expiradas
python manage.py clearsessions

# Verificar configurações
python manage.py check

# Shell interativo
python manage.py shell
```

### Monitoramento e Logs

#### Logs da Aplicação

Os logs são armazenados em `/app/logs/django.log` e incluem:

- Requisições HTTP
- Erros de aplicação
- Operações de banco de dados
- Autenticação e autorização

#### Configuração de Logging

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/django.log',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
}
```

## 💻 Desenvolvimento

### Configuração do Ambiente de Desenvolvimento

1. **Instale as dependências de desenvolvimento**
```bash
pip install -r requirements-dev.txt  # Se existir
```

2. **Configure o banco de desenvolvimento**
```bash
# Use SQLite para desenvolvimento rápido
python manage.py migrate

# Ou PostgreSQL local
createdb estagios_dev
export DATABASE_URL="postgresql://user:pass@localhost/estagios_dev"
python manage.py migrate
```

3. **Execute os testes**
```bash
python manage.py test
```

4. **Execute com debug ativo**
```bash
export DEBUG=True
python manage.py runserver 0.0.0.0:8000
```

### Estrutura de Desenvolvimento

#### Adicionando Novos Modelos

1. Crie o modelo em `core/models.py`
2. Crie as migrações: `python manage.py makemigrations`
3. Aplique as migrações: `python manage.py migrate`
4. Registre no admin em `core/admin.py`
5. Crie serializers em `core/serializers.py`
6. Crie views em `core/views.py`
7. Configure URLs em `core/urls.py`

#### Adicionando Novos Endpoints

```python
# Em core/views.py
@action(detail=True, methods=['post'])
def minha_acao(self, request, pk=None):
    obj = self.get_object()
    # Lógica da ação
    return Response({'status': 'success'})

# Em core/urls.py
# As rotas são criadas automaticamente pelo router
```

#### Testes

```python
# Em core/tests.py
from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class EstagiarioTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'test@test.com', 'pass')
        self.client.force_authenticate(user=self.user)
    
    def test_create_estagiario(self):
        data = {
            'nome': 'Teste',
            'email': 'teste@email.com',
            # ... outros campos
        }
        response = self.client.post('/api/v1/estagiarios/', data)
        self.assertEqual(response.status_code, 201)
```

### Debugging

#### Django Debug Toolbar (Opcional)

```python
# settings.py
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INTERNAL_IPS = ['127.0.0.1']
```

#### Logging Personalizado

```python
import logging
logger = logging.getLogger(__name__)

def minha_view(request):
    logger.info(f'Usuário {request.user} acessou a view')
    # ... lógica da view
```

## 🚀 Produção

### Configurações de Produção

#### Variáveis de Ambiente Obrigatórias

```env
DEBUG=False
SECRET_KEY=sua-chave-secreta-muito-forte-aqui
DATABASE_URL=postgresql://user:password@host:port/database
ALLOWED_HOSTS=seu-dominio.com,www.seu-dominio.com
```

#### Configurações de Segurança

```python
# settings.py para produção
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### Deploy com Docker

#### 1. Preparação

```bash
# Clone o repositório no servidor
git clone <url-do-repositorio>
cd estagios_system

# Configure variáveis de produção
cp .env.example .env
# Edite .env com configurações de produção
```

#### 2. SSL/TLS (HTTPS)

```bash
# Gere certificados SSL (exemplo com Let's Encrypt)
certbot certonly --standalone -d seu-dominio.com

# Copie os certificados
cp /etc/letsencrypt/live/seu-dominio.com/fullchain.pem docker/nginx/ssl/cert.pem
cp /etc/letsencrypt/live/seu-dominio.com/privkey.pem docker/nginx/ssl/key.pem
```

#### 3. Deploy

```bash
# Execute com perfil de produção
docker-compose --profile production up -d

# Verifique os logs
docker-compose logs -f web
docker-compose logs -f nginx
```

#### 4. Backup do Banco de Dados

```bash
# Backup
docker-compose exec db pg_dump -U estagios_user estagios_db > backup.sql

# Restore
docker-compose exec -T db psql -U estagios_user estagios_db < backup.sql
```

### Monitoramento em Produção

#### Health Checks

O Docker Compose inclui health checks para:
- **Aplicação Django**: Verifica se `/admin/` responde
- **PostgreSQL**: Verifica conectividade do banco
- **Nginx**: Verifica se o proxy está funcionando

#### Logs Centralizados

```bash
# Ver logs em tempo real
docker-compose logs -f

# Logs específicos
docker-compose logs web
docker-compose logs db
docker-compose logs nginx
```

#### Métricas e Alertas

Para produção, considere implementar:
- **Prometheus + Grafana**: Métricas de sistema
- **Sentry**: Monitoramento de erros
- **ELK Stack**: Análise de logs
- **Uptime monitoring**: Verificação de disponibilidade

### Escalabilidade

#### Horizontal Scaling

```yaml
# docker-compose.yml
services:
  web:
    deploy:
      replicas: 3
    # ... outras configurações
```

#### Load Balancer

```nginx
# nginx.conf
upstream django {
    server web1:8000;
    server web2:8000;
    server web3:8000;
}
```

#### Cache com Redis

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

## 🤝 Contribuição

### Como Contribuir

1. **Fork** o repositório
2. **Crie uma branch** para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. **Commit** suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. **Push** para a branch (`git push origin feature/nova-funcionalidade`)
5. **Abra um Pull Request**

### Padrões de Código

- **PEP 8**: Siga as convenções Python
- **Docstrings**: Documente classes e métodos
- **Type Hints**: Use anotações de tipo quando possível
- **Testes**: Inclua testes para novas funcionalidades

### Estrutura de Commits

```
tipo(escopo): descrição curta

Descrição mais detalhada se necessário.

- Lista de mudanças
- Outra mudança

Closes #123
```

**Tipos de commit:**
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `style`: Formatação
- `refactor`: Refatoração
- `test`: Testes
- `chore`: Tarefas de manutenção

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

## 📞 Suporte

Para dúvidas, problemas ou sugestões:

- **Issues**: Abra uma issue no GitHub
- **Email**: contato@sistema-estagios.com
- **Documentação**: Consulte este README

## 🔄 Changelog

### v1.0.0 (2024-01-XX)
- ✨ Implementação inicial do sistema
- 🔐 Autenticação JWT
- 📊 Painel administrativo
- 🐳 Containerização Docker
- 📚 Documentação completa

---

**Desenvolvido com ❤️ para facilitar o gerenciamento de estágios supervisionados.**



### Erro de Configuração PostgreSQL (`pg_stat_statements.track`)

Se você encontrar um erro relacionado a `pg_stat_statements.track` ao iniciar o Docker Compose, isso significa que uma configuração inválida foi aplicada ao PostgreSQL. Para corrigir, siga estes passos:

1. **Edite o arquivo `docker/postgres/init.sql`**:
   - Abra o arquivo e certifique-se de que a linha `ALTER SYSTEM SET pg_stat_statements.track = 'all';` esteja **comentada ou removida**.
   - Apenas a criação da extensão deve permanecer:
     ```sql
     CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";
     ```

2. **Re-inicialize o Docker Compose com volumes limpos**:
   ```bash
   docker-compose down --volumes
   docker-compose up --build
   ```
   Este comando irá remover os volumes de dados existentes (incluindo a configuração inválida do PostgreSQL) e reconstruir os serviços, aplicando a configuração corrigida.

**Explicação**: O parâmetro `pg_stat_statements.track` não pode ser definido via `ALTER SYSTEM` em algumas versões do PostgreSQL ou quando a extensão não está completamente carregada. A remoção dessa linha do `init.sql` e a re-inicialização limpa garantem que o banco de dados seja configurado corretamente desde o início.

