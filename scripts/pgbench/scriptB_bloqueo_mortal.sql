-- PGBENCH SCRIPT B: Deadlock Reproducible

-- Propósito: Provocar un deadlock real bajo carga concurrente

-- Fase 1: Script que GENERA deadlocks
-- Fase 2: Script CORREGIDO que elimina deadlocks mediante orden de locks


-- TODO: Implementar script que provoca deadlock:
-- Ejemplo: Transacción A bloquea tabla X luego Y
--          Transacción B bloquea tabla Y luego X
-- -> Resultado: deadlock

-- TODO: Implementar versión corregida con orden consistente de locks

-- Ejemplo de ejecución:
-- pgbench -d pagila -c 20 -j 4 -T 30 -f scripts/pgbench/scriptB_deadlock.sql
