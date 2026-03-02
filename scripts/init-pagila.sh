#!/bin/bash

set -e


echo "Iniciando carga de base de datos pagila"


echo "Descargando pagila.sql..."
wget -q https://raw.githubusercontent.com/neondatabase/postgres-sample-dbs/main/pagila.sql -O /tmp/pagila.sql

if [ ! -f /tmp/pagila.sql ]; then
    echo "ERROR: No se pudo descargar pagila.sql"
    exit 1
fi

echo "Archivo descargado exitosamente"

echo "Cargando datos de pagila en la base de datos..."
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -f /tmp/pagila.sql


echo "Base de datos pagila cargada exitosamente"


rm /tmp/pagila.sql

echo "Inicialización completada"
