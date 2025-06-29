-- Script de inicialização do PostgreSQL para o Sistema de Estágios

-- Criar extensões úteis
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

-- Configurações de performance
ALTER SYSTEM SET shared_preload_libraries = 'pg_stat_statements';

-- Configurar timezone
SET timezone = 'America/Sao_Paulo';

-- Criar índices para melhor performance (serão aplicados após as migrações)
-- Os índices específicos serão criados automaticamente pelo Django


