# Intersemestral-pagila-dvd-rental-api

API REST para sistema de renta de DVDs usando PostgreSQL (base de datos Pagila), FastAPI y SQLAlchemy Core. Proyecto intersemestral de Base de Datos Avanzadas enfocado en control de concurrencia, transacciones ACID, triggers, índices avanzados y pruebas de carga con pgbench.

## Características implementadas

### API REST (FastAPI)
- POST /rentals - Crear renta con control de concurrencia
- POST /returns/{rental_id} - Registrar devolución (idempotente)
- POST /payments - Registrar pago con validaciones

### Control de Concurrencia
- Índice UNIQUE parcial: `idx_rental_inventory_active`
- Sistema de reintentos con backoff exponencial
- Manejo de deadlocks y serialization failures
- Transacciones explícitas con SQLAlchemy Core

### Consultas SQL Avanzadas 
- Q1: RANK() - Top 10 clientes por pagos
- Q2: ROW_NUMBER() + PARTITION BY - Top 3 películas por tienda
- Q3: CTE - Inventario disponible por tienda
- Q4: CTE - Rentas tardías por categoría
- Q5: Detección de pagos sospechosos
- Q6: HAVING - Clientes con mora
- Q7: Validación de integridad (0 duplicados)

### Triggers
- Auditoría: Registra INSERT/UPDATE/DELETE en `registro_auditoria`
- Validación: Previene rentas si cliente tiene mora >7 días

### Índices (11 totales)
- Índice UNIQUE parcial (prevención duplicados)
- Índices compuestos (customer+date, inventory+return)
- Índices parciales (WHERE amount > 10, WHERE active = 1)

### Pruebas de Concurrencia (pgbench)
- Script A: Contención alta (inventario caliente)
- Script B: Prevención de deadlocks (orden consistente)

# Instalación y ejecución

## Prerequisitos

- Docker Desktop instalado y corriendo
- Puertos disponibles: 8000 (API), 5432 (PostgreSQL)
- Git para clonar el repositorio

## Paso 1: Clonar y levantar el proyecto

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/Intersemestral-pagila-dvd-rental-api.git
cd Intersemestral-pagila-dvd-rental-api

# Levantar contenedores (incluye carga automática de DB Pagila)
docker-compose up -d

# Verificar que los contenedores estén corriendo
docker ps
```

Deberías ver 2 contenedores: `pagila-api` y `pagila-db` en estado "Up"

## Paso 2: Aplicar índices y triggers

```bash
# Copiar archivos SQL al contenedor
docker cp sql/indices.sql pagila-db:/tmp/indices.sql
docker cp sql/disparadores.sql pagila-db:/tmp/disparadores.sql

# Aplicar índices (incluye idx_rental_inventory_active UNIQUE)
docker exec -i pagila-db psql -U postgres -d pagila -f /tmp/indices.sql

# Aplicar triggers (auditoría + validación rentas vencidas)
docker exec -i pagila-db psql -U postgres -d pagila -f /tmp/disparadores.sql
```

## Paso 3: Verificar la API

Acceder a Swagger UI: **http://localhost:8000/docs**

### Probar endpoints:

**1. Crear renta:**
```bash
curl -X POST "http://localhost:8000/rentals/" -H "Content-Type: application/json" -d "{\"inventory_id\": 200, \"customer_id\": 1, \"staff_id\": 1}"
```

**2. Registrar devolución:**
```bash
curl -X POST "http://localhost:8000/returns/16056"
```

**3. Registrar pago:**
```bash
curl -X POST "http://localhost:8000/payments/" -H "Content-Type: application/json" -d "{\"customer_id\": 1, \"staff_id\": 1, \"rental_id\": 16056, \"amount\": 4.99}"
```

## Paso 4: Ejecutar las 7 consultas SQL

```bash
# Copiar archivo de consultas
docker cp sql/consultas.sql pagila-db:/tmp/consultas.sql

# Ejecutar todas las consultas
docker exec -i pagila-db psql -U postgres -d pagila -f /tmp/consultas.sql

# O ejecutar consultas individuales:
docker exec -i pagila-db psql -U postgres -d pagila -c "SELECT RANK() OVER (ORDER BY SUM(p.amount) DESC) AS ranking, c.customer_id, c.first_name, SUM(p.amount) AS total_pagado FROM customer c JOIN payment p ON c.customer_id = p.customer_id GROUP BY c.customer_id, c.first_name, c.last_name ORDER BY total_pagado DESC LIMIT 10;"
```

## Paso 5: Ejecutar pruebas de concurrencia (pgbench)

```bash
# Copiar scripts de pgbench al contenedor
docker exec -i pagila-db mkdir -p /tmp/pgbench
docker cp scripts/pgbench/scriptA_inventario_caliente.sql pagila-db:/tmp/pgbench/
docker cp scripts/pgbench/scriptB_bloqueo_mortal.sql pagila-db:/tmp/pgbench/

# Script A: Prueba de contención (Hot Inventory)
docker exec -i pagila-db pgbench -U postgres -d pagila -f /tmp/pgbench/scriptA_inventario_caliente.sql -c 10 -j 2 -t 100 -r

# Script B: Prueba de deadlocks
docker exec -i pagila-db pgbench -U postgres -d pagila -f /tmp/pgbench/scriptB_bloqueo_mortal.sql -c 20 -j 4 -t 50 -r
```

**Resultados esperados Script A:**
- 1,000 transacciones procesadas
- TPS: ~1,300-1,500
- 0% transacciones fallidas
- Solo 5 rentas insertadas (resto rechazadas por disponibilidad)

**Resultados esperados Script B:**
- 1,000 transacciones procesadas
- TPS: ~2,000-2,500
- 0 deadlocks (orden consistente de locks)

## Paso 6: Verificar integridad (Query 7)

```bash
# Verificar que NO existen rentas activas duplicadas
docker exec -i pagila-db psql -U postgres -d pagila -c "SELECT inventory_id, COUNT(*) AS rentas_activas FROM rental WHERE return_date IS NULL GROUP BY inventory_id HAVING COUNT(*) > 1;"
```

**Resultado esperado:** `0 rows` ✅ (sin duplicados)

## Verificar triggers

```bash
# Ver registros de auditoría
docker exec -i pagila-db psql -U postgres -d pagila -c "SELECT * FROM registro_auditoria ORDER BY fecha_evento DESC LIMIT 10;"

# Probar trigger de validación (debería fallar)
docker exec -i pagila-db psql -U postgres -d pagila -c "INSERT INTO rental (rental_date, inventory_id, customer_id, staff_id) VALUES (NOW() - INTERVAL '10 days', 100, 1, 1); INSERT INTO rental (rental_date, inventory_id, customer_id, staff_id) VALUES (NOW(), 101, 1, 1);"
```

## Detener el proyecto

```bash
docker-compose down
```

## Instalación manual (sin Docker)

```bash
# Instalar dependencias
pip install -r requisitos.txt

# Configurar variables de entorno
export DATABASE_HOST=localhost
export DATABASE_PORT=5432
export DATABASE_USER=postgres
export DATABASE_PASSWORD=postgres
export DATABASE_NAME=pagila

# Levantar API
uvicorn app.principal:app --reload --host 0.0.0.0 --port 8000
```

## Acceso a servicios

- **API (Swagger UI):** http://localhost:8000/docs
- **API (ReDoc):** http://localhost:8000/redoc
- **Base de datos:** `postgresql://postgres:postgres@localhost:5432/pagila`

# Tecnologías

* PostgreSQL 15 (con MVCC para control de concurrencia)
* FastAPI 0.109.0 (API REST asíncrona)
* SQLAlchemy 2.0.25 Core (sin ORM - SQL raw)
* Pydantic 2.5.0 (validación de datos)
* Docker Compose (orquestación de contenedores)
* pgbench (pruebas de carga PostgreSQL)

## Resultados cuantitativos

### Rendimiento
- **TPS máximo:** 2,308 transacciones/segundo (Script B)
- **Latencia promedio:** 7-8 ms bajo alta concurrencia
- **Transacciones exitosas:** 2,000/2,000 (100%)
- **Transacciones fallidas:** 0 (0.000%)

### Integridad
- **Rentas activas duplicadas:** 0 (Query 7)
- **Deadlocks detectados:** 0 (orden consistente de locks)
- **Registros de auditoría:** 6+ operaciones capturadas

### Concurrencia
- **Clientes concurrentes probados:** 20 simultáneos
- **Transacciones por prueba:** 1,000
- **Contención extrema:** 10 clientes → 5 DVDs (80% rechazo esperado)

### Optimización
- **Índices creados:** 11 personalizados
- **Tiempo consultas críticas:** < 1 ms
- **Ahorro espacio índices parciales:** ~90% vs índices completos


## Estructura del código

```
Intersemestral-pagila-dvd-rental-api/
├── app/
│   ├── __init__.py
│   ├── principal.py              # Configuración FastAPI
│   ├── base_datos.py             # Conexión PostgreSQL
│   ├── configuracion.py          # Variables de entorno
│   ├── esquemas.py               # Modelos Pydantic
│   ├── modelos.py                # Definiciones SQLAlchemy
│   ├── rutas/
│   │   ├── rentas.py             # POST /rentals
│   │   ├── devoluciones.py       # POST /returns/{id}
│   │   └── pagos.py              # POST /payments
│   ├── servicios/
│   │   ├── servicio_rentas.py    # Lógica de negocio
│   │   ├── servicio_devoluciones.py
│   │   └── servicio_pagos.py
│   └── utilidades/
│       ├── reintentos.py         # Backoff exponencial
│       └── transacciones.py      # Control transaccional
├── sql/
│   ├── consultas.sql             # 7 queries avanzadas
│   ├── disparadores.sql          # 2 triggers
│   └── indices.sql               # 11 índices
├── scripts/
│   ├── pgbench/
│   │   ├── scriptA_inventario_caliente.sql
│   │   └── scriptB_bloqueo_mortal.sql
│   └── init-pagila.sh            # Carga inicial DB
├── docker-compose.yml            # Orquestación
├── Dockerfile                    # Imagen API
├── requisitos.txt               # Dependencias Python
└── README.md                    # Este archivo
```

## Troubleshooting

### Error: "Port 5432 already in use"
```bash
# Detener PostgreSQL local
sudo service postgresql stop  # Linux
brew services stop postgresql  # macOS

# O cambiar puerto en docker-compose.yml
ports:
  - "5433:5432"  # Usar 5433 externamente
```

### Error: "API no responde en localhost:8000"
```bash
# Verificar logs del contenedor
docker logs pagila-api

# Verificar que DATABASE_URL está configurado
docker exec -i pagila-api env | grep DATABASE
```

### Error: "relation does not exist" al ejecutar queries
```bash
# Aplicar índices y triggers primero (Paso 2)
docker exec -i pagila-db psql -U postgres -d pagila -f /tmp/indices.sql
docker exec -i pagila-db psql -U postgres -d pagila -f /tmp/disparadores.sql
```

### Limpiar y reiniciar proyecto
```bash
# Eliminar todo (contenedores + volúmenes)
docker-compose down -v

# Reconstruir desde cero
docker-compose up -d --build

# Volver a aplicar índices y triggers
# (repetir Paso 2)
```



