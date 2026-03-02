-- PGBENCH SCRIPT A: Hot Inventory Contention

-- Propósito: Simular contención cuando múltiples clientes intentan rentar
-- el mismo inventory_id simultáneamente

-- Expectativa: Solo una transacción debe concretarse, el resto debe fallar
-- o esperar. Al final NO debe haber rentas activas duplicadas.


-- TODO: Implementar script que:
-- 1. Selecciona un inventory_id específico (hot item)
-- 2. Verifica disponibilidad (return_date IS NULL check)
-- 3. Inserta nueva renta
-- Todo dentro de una transacción

-- Ejemplo de ejecución:
-- pgbench -d pagila -c 20 -j 4 -T 30 -f scripts/pgbench/scriptA_hot_inventory.sql
