param(
    [string]$ServidorBD = "localhost",
    [string]$PuertoBD = "5432",
    [string]$NombreBD = "pagila",
    [string]$UsuarioBD = "postgres"
)

Write-Host "Pruebas de Concurrencia con pgbench" 
Write-Host ""

$ScriptA = "scripts\pgbench\scriptA_inventario_caliente.sql"
$ScriptB = "scripts\pgbench\scriptB_bloqueo_mortal.sql"

Write-Host "Script A: Hot Inventory" 
Write-Host "Simulando 20 clientes intentando rentar el mismo inventario."
Write-Host ""

pgbench -h $ServidorBD -p $PuertoBD -U $UsuarioBD -d $NombreBD -c 20 -j 4 -T 30 -f $ScriptA

Write-Host ""
Write-Host "Verificando integridad" 
$QueryVerificar = "SELECT inventory_id, COUNT(*) as rentas_activas FROM rental WHERE return_date IS NULL GROUP BY inventory_id HAVING COUNT(*) > 1;"

psql -h $ServidorBD -p $PuertoBD -U $UsuarioBD -d $NombreBD -c $QueryVerificar

Write-Host ""
Write-Host "Script B: Deadlock Reproducible" 
Write-Host "Provocando deadlocks con acceso cruzado..."
Write-Host ""

pgbench -h $ServidorBD -p $PuertoBD -U $UsuarioBD -d $NombreBD -c 20 -j 4 -T 30 -f $ScriptB

Write-Host ""
Write-Host "Pruebas completadas" 
