$DB_USER = "postgres"
$DB_HOST = "localhost"
$DB_PORT = "5432"
$DB_NAME = "pagila"
$PAGILA_URL = "https://raw.githubusercontent.com/neondatabase/postgres-sample-dbs/main/pagila.sql"
$TEMP_SQL = "pagila_temp.sql"

Write-Host "[1/5] Creando base de datos '$DB_NAME'"
try {
    createdb -U $DB_USER -h $DB_HOST -p $DB_PORT $DB_NAME 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Base de datos creada exitosamente" -ForegroundColor Green
    } else {
        Write-Host "Base de datos ya existe, continuando" -ForegroundColor Yellow
    }
} catch {
    Write-Host "Base de datos ya existe, continuando" -ForegroundColor Yellow
}

Write-Host "[2/5] Descargando esquema de Pagila"
try {
    Invoke-WebRequest -Uri $PAGILA_URL -OutFile $TEMP_SQL -ErrorAction Stop
    Write-Host "Archivo descargado exitosamente" -ForegroundColor Green
} catch {
    Write-Host "Error al descargar el archivo" -ForegroundColor Red
    exit 1
}

Write-Host "[3/5] Cargando datos de Pagila"
try {
    psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f $TEMP_SQL
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Datos cargados exitosamente" -ForegroundColor Green
    } else {
        Write-Host "Error al cargar datos" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "Error al ejecutar psql" -ForegroundColor Red
    exit 1
}

Write-Host "[4/5] Ejecutando disparadores"
if (Test-Path "sql/disparadores.sql") {
    psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f sql/disparadores.sql
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Disparadores creados exitosamente" -ForegroundColor Green
    } else {
        Write-Host "Error al crear disparadores" -ForegroundColor Red
    }
} else {
    Write-Host "Archivo disparadores.sql no encontrado, omitiendo" -ForegroundColor Yellow
}

Write-Host "[5/5] Ejecutando indices"
if (Test-Path "sql/indices.sql") {
    psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f sql/indices.sql
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Indices creados exitosamente" -ForegroundColor Green
    } else {
        Write-Host "Error al crear indices" -ForegroundColor Red
    }
} else {
    Write-Host "Archivo indices.sql no encontrado, omitiendo" -ForegroundColor Yellow
}

if (Test-Path $TEMP_SQL) {
    Remove-Item $TEMP_SQL -Force
    Write-Host "Archivo temporal eliminado" -ForegroundColor Green
}

Write-Host "Configuracion completada exitosamente" -ForegroundColor Green
