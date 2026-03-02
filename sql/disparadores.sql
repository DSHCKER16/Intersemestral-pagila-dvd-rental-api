
-- TRIGGERS - PAGILA DVD RENTAL
-- Archivo de triggers para auditoría y reglas de negocio




-- TRIGGER 1: AUDITORÍA
-- Propósito: Registrar INSERT/UPDATE/DELETE sobre rental y payment


-- TODO: Crear tabla audit_log
-- CREATE TABLE audit_log (
--     id SERIAL PRIMARY KEY,
--     event_ts TIMESTAMP DEFAULT NOW(),
--     table_name VARCHAR(50),
--     operation VARCHAR(10),
--     pk_value INTEGER,
--     old_row JSONB,
--     new_row JSONB
-- );

-- TODO: CREATE FUNCTION para trigger de auditoría

-- TODO: CREATE TRIGGER para rental

-- TODO: CREATE TRIGGER para payment



-- TRIGGER 2: REGLA DE NEGOCIO

-- Propósito: Implementar una de las siguientes opciones:
-- Opción A: Impedir renta si el cliente supera X rentas activas
-- Opción B: Impedir pago <= 0 o fuera de rango permitido
-- Opción C: Bloquear renta si el cliente tiene rentas vencidas sin devolver


-- TODO: Seleccionar y documentar la opción elegida
-- TODO: CREATE FUNCTION para trigger de regla de negocio
-- TODO: CREATE TRIGGER
