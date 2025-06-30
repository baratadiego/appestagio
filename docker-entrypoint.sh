#!/bin/bash
set -e
: "${POSTGRES_HOST:=db}"
: "${POSTGRES_PORT:=5432}"
: "${POSTGRES_USER:=postgres}"

# Função para aguardar o banco de dados
wait_for_db() {
    echo "Aguardando banco de dados..."
    until pg_isready -h $POSTGRES_HOST -U $POSTGRES_USER; do
      echo "Waiting for postgres..."
      sleep 2
    done
    echo "Banco de dados está pronto!"
}

# Função para executar migrações
run_migrations() {
    echo "Executando migrações..."
    python manage.py migrate --noinput
}

# Função para coletar arquivos estáticos
collect_static() {
    echo "Coletando arquivos estáticos..."
    python manage.py collectstatic --noinput
}

# Função para criar dados iniciais
setup_initial_data() {
    echo "Configurando dados iniciais..."
    python manage.py setup_initial_data --create-superuser --create-sample-data
}

# Aguardar banco de dados se estiver usando PostgreSQL
if [ "$DATABASE_URL" ]; then
    wait_for_db
fi

# Executar migrações
run_migrations

# Coletar arquivos estáticos
collect_static

# Configurar dados iniciais (apenas se não existir superusuário)
if [ "$SETUP_INITIAL_DATA" = "true" ]; then
    setup_initial_data
fi

# Executar comando passado como argumento
exec "$@"

