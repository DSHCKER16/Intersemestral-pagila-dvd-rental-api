SELECT 
    RANK() OVER (ORDER BY SUM(p.amount) DESC) AS ranking,
    c.customer_id,
    c.first_name AS nombre,
    c.last_name AS apellido,
    SUM(p.amount) AS total_pagado
FROM customer c
JOIN payment p ON c.customer_id = p.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY total_pagado DESC
LIMIT 10;

SELECT 
    tienda_id,
    pelicula_id,
    titulo,
    cantidad_rentas,
    fila
FROM (
    SELECT 
        i.store_id AS tienda_id,
        f.film_id AS pelicula_id,
        f.title AS titulo,
        COUNT(r.rental_id) AS cantidad_rentas,
        ROW_NUMBER() OVER (PARTITION BY i.store_id ORDER BY COUNT(r.rental_id) DESC) AS fila
    FROM film f
    JOIN inventory i ON f.film_id = i.film_id
    JOIN rental r ON i.inventory_id = r.inventory_id
    GROUP BY i.store_id, f.film_id, f.title
) AS ranking_peliculas
WHERE fila <= 3
ORDER BY tienda_id, fila;

WITH inventario_activo AS (
    SELECT 
        i.inventory_id,
        i.store_id,
        CASE 
            WHEN r.rental_id IS NULL OR r.return_date IS NOT NULL 
            THEN 1 
            ELSE 0 
        END AS disponible
    FROM inventory i
    LEFT JOIN rental r ON i.inventory_id = r.inventory_id
        AND r.return_date IS NULL
)
SELECT 
    store_id AS tienda_id,
    SUM(disponible) AS inventario_disponible
FROM inventario_activo
GROUP BY store_id
ORDER BY tienda_id;

WITH rentas_tardias AS (
    SELECT 
        r.rental_id,
        r.customer_id,
        r.rental_date,
        r.return_date,
        f.film_id,
        f.rental_duration,
        (r.rental_date + INTERVAL '1 day' * f.rental_duration) AS fecha_limite,
        EXTRACT(DAY FROM (r.return_date - (r.rental_date + INTERVAL '1 day' * f.rental_duration))) AS dias_retraso
    FROM rental r
    JOIN inventory i ON r.inventory_id = i.inventory_id
    JOIN film f ON i.film_id = f.film_id
    WHERE r.return_date IS NOT NULL
        AND r.return_date > (r.rental_date + INTERVAL '1 day' * f.rental_duration)
)
SELECT 
    c.category_id AS categoria_id,
    c.name AS nombre_categoria,
    COUNT(rt.rental_id) AS rentas_tardias,
    ROUND(AVG(rt.dias_retraso), 2) AS promedio_dias_retraso
FROM rentas_tardias rt
JOIN inventory i ON rt.film_id = i.film_id
JOIN film f ON i.film_id = f.film_id
JOIN film_category fc ON f.film_id = fc.film_id
JOIN category c ON fc.category_id = c.category_id
GROUP BY c.category_id, c.name
ORDER BY rentas_tardias DESC;

SELECT 
    p.payment_id AS pago_id,
    p.customer_id AS cliente_id,
    p.amount AS monto,
    p.payment_date AS fecha_pago,
    CASE 
        WHEN p.amount > 10 THEN 'Monto alto sospechoso'
        WHEN pagos_dia > 5 THEN 'Múltiples pagos mismo día'
        ELSE 'Normal'
    END AS razon_alerta
FROM payment p
JOIN (
    SELECT 
        customer_id,
        DATE(payment_date) AS fecha,
        COUNT(*) AS pagos_dia
    FROM payment
    GROUP BY customer_id, DATE(payment_date)
) AS conteo_pagos ON p.customer_id = conteo_pagos.customer_id 
    AND DATE(p.payment_date) = conteo_pagos.fecha
WHERE p.amount > 10 OR conteo_pagos.pagos_dia > 5
ORDER BY p.payment_date DESC;

SELECT 
    c.customer_id AS cliente_id,
    c.first_name AS nombre,
    c.last_name AS apellido,
    COUNT(r.rental_id) AS cantidad_rentas_tardias,
    MAX(r.return_date) AS ultima_devolucion_tardia
FROM customer c
JOIN rental r ON c.customer_id = r.customer_id
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f ON i.film_id = f.film_id
WHERE r.return_date IS NOT NULL
    AND r.return_date > (r.rental_date + INTERVAL '1 day' * f.rental_duration)
GROUP BY c.customer_id, c.first_name, c.last_name
HAVING COUNT(r.rental_id) >= 2
ORDER BY cantidad_rentas_tardias DESC;

SELECT 
    inventory_id AS inventario_id,
    COUNT(*) AS rentas_activas,
    ARRAY_AGG(rental_id) AS ids_rentas
FROM rental
WHERE return_date IS NULL
GROUP BY inventory_id
HAVING COUNT(*) > 1
ORDER BY rentas_activas DESC;
