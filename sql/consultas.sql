-- SQL QUERIES - PAGILA DVD RENTAL

-- Archivo de consultas avanzadas usando Window Functions y CTEs




-- Q1: Top 10 clientes por gasto con ranking (WINDOW FUNCTION)

-- Propósito: Obtener los 10 clientes que más han gastado en rentas
-- Técnica: RANK() OVER window function


-- TODO: Implementar consulta con RANK() o DENSE_RANK()
-- Columnas requeridas: rank, customer_id, first_name, last_name, total_paid



-- Q2: Top 3 películas por tienda (WINDOW FUNCTION)

-- Propósito: Obtener las 3 películas más rentadas por cada tienda
-- Técnica: ROW_NUMBER() OVER (PARTITION BY store_id)


-- TODO: Implementar consulta con ROW_NUMBER() y PARTITION BY
-- Columnas requeridas: store_id, film_id, title, rentals_count, rn



-- Q3: Inventario disponible por tienda (CTE)

-- Propósito: Calcular cuántos items están disponibles por tienda
-- (no rentados actualmente, es decir, return_date IS NOT NULL o no en rental)
-- Técnica: Common Table Expression (CTE)


-- TODO: Implementar consulta con CTE
-- Columnas requeridas: store_id, available_inventory_count



-- Q4: Análisis de retrasos - Rentas tardías por categoría (CTE)

-- Propósito: Analizar rentas tardías agregadas por categoría de película
-- Técnica: CTE para calcular rentas tardías + agregación


-- TODO: Implementar consulta con CTE para late rentals
-- Columnas requeridas: category_id, category_name, late_rentals, avg_days_late



-- Q5: Auditoría - Pagos sospechosos

-- Propósito: Detectar pagos inusuales o potencialmente fraudulentos
-- Ejemplos: pagos muy altos, pagos duplicados mismo día
-- Técnica: Agregación + HAVING + lógica de detección


-- TODO: Implementar consulta con lógica de detección
-- Columnas requeridas: payment_id, customer_id, amount, payment_date, flag_reason



-- Q6: Clientes con riesgo (mora)

-- Propósito: Identificar clientes con múltiples rentas tardías
-- Definición tardía: return_date > rental_date + film.rental_duration
-- Técnica: Joins + cálculo de due_date + HAVING


-- TODO: Implementar consulta con cálculo de due date
-- Columnas requeridas: customer_id, late_returns_count, last_late_return_date



-- Q7: Integridad - Inventario con rentas activas duplicadas

-- Propósito: Detectar inconsistencias de inventarios con más de 1 renta activa
-- (return_date IS NULL)
-- Técnica: Agregación + HAVING COUNT(*) > 1


-- TODO: Implementar consulta de validación de integridad
-- Columnas requeridas: inventory_id, active_rentals_count, rental_ids
