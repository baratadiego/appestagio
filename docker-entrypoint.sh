#!/bin/sh
set -e

echo "Aguardando banco de dados..."

# Aguarda até que o Postgres responda em db:5432
until pg_isready -h "${POSTGRES_HOST:-db}" -p "${POSTGRES_PORT:-5432}" -U "${POSTGRES_USER}"; do
  echo "Aguardando banco de dados..."
  sleep 2
done

echo "Banco de dados está pronto!"

# Roda migrações, coleta estáticos e dados iniciais
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Se configurado para inicializar dados
if [ "${SETUP_INITIAL_DATA}" = "true" ]; then
  python manage.py setup_initial_data
fi

# Inicia o Gunicorn
exec gunicorn estagios.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3
