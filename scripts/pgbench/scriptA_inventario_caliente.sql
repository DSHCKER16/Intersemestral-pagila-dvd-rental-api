\set inventory_final random_exponential(1, 5, 4.0)
\set cliente_aleatorio random(1, 599)
\set staff_aleatorio random(1, 2)

BEGIN;

SELECT i.inventory_id, i.film_id
FROM inventory i
WHERE i.inventory_id = :inventory_final
FOR UPDATE;

INSERT INTO rental (rental_date, inventory_id, customer_id, staff_id, last_update)
SELECT NOW(), 
       :inventory_final, 
       :cliente_aleatorio, 
       :staff_aleatorio, 
       NOW()
WHERE NOT EXISTS (
    SELECT 1 
    FROM rental 
    WHERE inventory_id = :inventory_final
    AND return_date IS NULL
);

COMMIT;
