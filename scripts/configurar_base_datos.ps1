# ============================================================================
# Database Setup Script (PowerShell)
# ============================================================================
# Script para crear la base de datos Pagila y cargar datos en Windows
# ============================================================================

# TODO: Implementar comandos de setup:
# 1. Crear base de datos pagila
# 2. Descargar pagila.sql
# 3. Ejecutar psql para cargar datos
# 4. Ejecutar disparadores.sql
# 5. Ejecutar indices.sql

# Ejemplo de comandos:
# createdb -U postgres pagila
# Invoke-WebRequest -Uri "https://raw.githubusercontent.com/neondatabase/postgres-sample-dbs/main/pagila.sql" -OutFile "pagila.sql"
# psql -h localhost -p 5432 -U postgres -d pagila -f pagila.sql
# psql -h localhost -p 5432 -U postgres -d pagila -f sql/disparadores.sql
# psql -h localhost -p 5432 -U postgres -d pagila -f sql/indices.sql
