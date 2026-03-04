#!/bin/bash

set -e

DB_USER="postgres"
DB_HOST="localhost"
DB_PORT="5432"
DB_NAME="pagila"
PAGILA_URL="https://raw.githubusercontent.com/neondatabase/postgres-sample-dbs/main/pagila.sql"
TEMP_SQL="pagila_temp.sql"

echo "[1/5] Creando base de datos '$DB_NAME'..."
if createdb -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" "$DB_NAME" 2>/dev/null; then
    echo "Base de datos creada exitosamente"
else
    echo "Base de datos ya existe, continuando"
fi

echo "[2/5] Descargando esquema de Pagila"
if wget -q "$PAGILA_URL" -O "$TEMP_SQL"; then
    echo "Archivo descargado exitosamente"
else
    echo "Error al descargar el archivo"
    exit 1
fi

echo "[3/5] Cargando datos de Pagila"
if psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -f "$TEMP_SQL" > /dev/null; then
    echo "Datos cargados exitosamente"
else
    echo "Error al cargar datos"
    exit 1
fi

echo "[4/5] Ejecutando disparadores"
if [ -f "sql/disparadores.sql" ]; then
    if psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -f "sql/disparadores.sql" > /dev/null; then
        echo "Disparadores creados exitosamente"
    else
        echo "Error al crear disparadores"
    fi
else
    echo "Archivo disparadores.sql no encontrado, omitiendo"
fi

echo "[5/5] Ejecutando indices"
if [ -f "sql/indices.sql" ]; then
    if psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -f "sql/indices.sql" > /dev/null; then
        echo "Indices creados exitosamente"
    else
        echo "Error al crear indices"
    fi
else
    echo "Archivo indices.sql no encontrado, omitiendo"
fi

if [ -f "$TEMP_SQL" ]; then
    rm -f "$TEMP_SQL"
    echo "Archivo temporal eliminado"
fi

echo "Configuracion completada exitosamente"
