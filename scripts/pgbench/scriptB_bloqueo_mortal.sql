\set cliente_a random(1, 299)
\set cliente_b random(300, 599)
\set rental_a random(1, 5000)
\set rental_b random(5001, 10000)

BEGIN;

UPDATE customer 
SET last_update = NOW() 
WHERE customer_id = :cliente_a;

UPDATE customer 
SET last_update = NOW()
WHERE customer_id = :cliente_b;

UPDATE rental 
SET last_update = NOW() 
WHERE rental_id = :rental_a;

UPDATE rental 
SET last_update = NOW() 
WHERE rental_id = :rental_b;

COMMIT;
