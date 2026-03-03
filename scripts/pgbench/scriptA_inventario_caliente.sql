\set inventario_caliente 1
\set cliente_aleatorio random(1, 599)
\set staff_aleatorio random(1, 2)

BEGIN;

SELECT inventory_id 
FROM inventory 
WHERE inventory_id = :inventario_caliente 
  AND inventory_id NOT IN (
    SELECT inventory_id 
    FROM rental 
    WHERE return_date IS NULL
  )
FOR UPDATE;

INSERT INTO rental (rental_date, inventory_id, customer_id, staff_id, last_update)
SELECT NOW(), :inventario_caliente, :cliente_aleatorio, :staff_aleatorio, NOW()
WHERE EXISTS (
    SELECT 1 
    FROM inventory 
    WHERE inventory_id = :inventario_caliente 
      AND inventory_id NOT IN (
        SELECT inventory_id 
        FROM rental 
        WHERE return_date IS NULL
      )
);

COMMIT;
