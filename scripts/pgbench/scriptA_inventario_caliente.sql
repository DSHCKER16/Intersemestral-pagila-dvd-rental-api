\set inventario_caliente random(1, 5)
\set usar_hot_inventory random(1, 100)
\set inventory_final 1 + (:usar_hot_inventory <= 80) * 0 + (:usar_hot_inventory > 80) * (:inventario_caliente - 1)
\set cliente_aleatorio random(1, 599)
\set staff_aleatorio random(1, 2)

BEGIN;

DO $$
DECLARE
    v_disponible BOOLEAN;
    v_inventory_id INTEGER := :inventory_final;
BEGIN
    SELECT NOT EXISTS(
        SELECT 1 
        FROM rental 
        WHERE inventory_id = v_inventory_id 
        AND return_date IS NULL
    ) INTO v_disponible;
    
    IF NOT v_disponible THEN
        RAISE EXCEPTION 'INVENTORY_NOT_AVAILABLE: inventory_id % already rented', v_inventory_id
            USING ERRCODE = '23505';
    END IF;
END;
$$ LANGUAGE plpgsql;

SELECT i.inventory_id, i.film_id
FROM inventory i
WHERE i.inventory_id = :inventory_final
FOR UPDATE;

SELECT 1 
FROM inventory 
WHERE inventory_id = :inventory_final
  AND NOT EXISTS (
    SELECT 1 
    FROM rental 
    WHERE inventory_id = :inventory_final
    AND return_date IS NULL
  );

INSERT INTO rental (rental_date, inventory_id, customer_id, staff_id, last_update)
SELECT NOW(), 
       :inventory_final, 
       :cliente_aleatorio, 
       :staff_aleatorio, 
       NOW()
WHERE EXISTS (
    SELECT 1 
    FROM inventory 
    WHERE inventory_id = :inventory_final
      AND NOT EXISTS (
        SELECT 1 
        FROM rental r2
        WHERE r2.inventory_id = :inventory_final
        AND r2.return_date IS NULL
      )
);

DO $$
DECLARE
    v_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO v_count
    FROM rental
    WHERE inventory_id = :inventory_final
    AND return_date IS NULL;
    
    IF v_count > 1 THEN
        RAISE EXCEPTION 'INTEGRITY_VIOLATION: % active rentals for inventory %', v_count, :inventory_final;
    END IF;
END;
$$ LANGUAGE plpgsql;

COMMIT;
