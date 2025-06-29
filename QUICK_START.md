# 🚀 Guia de Início Rápido - Sistema de Estágios

## ⚡ Execução Imediata

### Opção 1: Docker (Recomendado)

```bash
# 1. Clone e entre no diretório
git clone <url-do-repositorio>
cd estagios_system

# 2. Execute com Docker
docker-compose up --build

# 3. Acesse o sistema
# - Aplicação: http://localhost:8000
# - Admin: http://localhost:8000/admin (admin/admin123)
# - pgAdmin: http://localhost:5050 (admin@estagios.com/admin123)
```

### Opção 2: Execução Local

```bash
# 1. Clone e configure
git clone <url-do-repositorio>
cd estagios_system
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# 2. Configure dados iniciais
python manage.py migrate
python manage.py setup_initial_data --create-superuser --create-sample-data

# 3. Execute o servidor
python manage.py runserver 0.0.0.0:8000
```

## 🔑 Credenciais Padrão

- **Admin Django**: `admin` / `admin123`
- **pgAdmin**: `admin@estagios.com` / `admin123`

## 📱 Endpoints Principais

### Autenticação
```bash
# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### API Endpoints
- **Estagiários**: `GET/POST /api/v1/estagiarios/`
- **Convênios**: `GET/POST /api/v1/convenios/`
- **Estágios**: `GET/POST /api/v1/estagios/`
- **Documentos**: `GET/POST /api/v1/documentos/`
- **Notificações**: `GET/POST /api/v1/notificacoes/`
- **Estatísticas**: `GET /api/v1/estatisticas/`

## 🎯 Funcionalidades Testáveis

### 1. Painel Admin
- Acesse: http://localhost:8000/admin
- Explore todas as entidades
- Teste filtros e buscas
- Veja estatísticas em tempo real

### 2. API REST
- Use Postman ou curl
- Teste autenticação JWT
- Explore endpoints CRUD
- Teste filtros e paginação

### 3. Dados de Exemplo
O sistema já vem com:
- 4 estagiários cadastrados
- 3 convênios ativos
- 3 estágios (2 em andamento, 1 finalizado)
- 3 notificações de exemplo

## 🔧 Comandos Úteis

```bash
# Resetar dados
python manage.py flush
python manage.py setup_initial_data --create-superuser --create-sample-data

# Ver logs (Docker)
docker-compose logs -f web

# Acessar shell Django
python manage.py shell

# Criar superusuário adicional
python manage.py createsuperuser
```

## 📊 Estrutura de Dados

### Estagiário
```json
{
  "nome": "Ana Carolina Silva",
  "email": "ana.silva@email.com",
  "telefone": "(11) 99999-1111",
  "curso": "Ciência da Computação",
  "periodo": "7º Semestre",
  "cpf": "123.456.789-01",
  "data_nascimento": "2000-05-15",
  "status": "ATIVO"
}
```

### Estágio
```json
{
  "estagiario": 1,
  "convenio": 1,
  "supervisor": "Carlos Mendes",
  "supervisor_email": "carlos.mendes@techcorp.com",
  "carga_horaria": 30,
  "data_inicio": "2024-01-15",
  "data_fim": "2024-07-15",
  "status": "EM_ANDAMENTO"
}
```

## 🚨 Solução de Problemas

### Erro de Porta
```bash
# Se a porta 8000 estiver ocupada
python manage.py runserver 0.0.0.0:8001
```

### Erro de Banco
```bash
# Resetar migrações
rm -rf core/migrations/0*.py
python manage.py makemigrations
python manage.py migrate
```

### Erro Docker
```bash
# Limpar containers
docker-compose down -v
docker-compose up --build
```

## 📞 Suporte

- **Documentação completa**: Veja `README.md`
- **Logs**: Verifique `logs/django.log`
- **Debug**: Configure `DEBUG=True` no `.env`

---

**Sistema pronto para uso! 🎉**

