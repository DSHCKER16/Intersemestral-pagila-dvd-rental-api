\set cliente_a random(1, 299)
\set cliente_b random(300, 599)
\set monto_aleatorio random(1, 10)
\set orden_aleatorio random(0, 1)
\set rental_a random(1, 5000)
\set rental_b random(5001, 10000)

BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;

\if :orden_aleatorio = 0
    UPDATE customer 
    SET last_update = NOW(), 
        active = active
    WHERE customer_id = :cliente_a;
    
    SELECT pg_sleep(0.002);
    
    UPDATE customer 
    SET last_update = NOW(),
        active = active
    WHERE customer_id = :cliente_b;
    
    UPDATE rental 
    SET last_update = NOW() 
    WHERE rental_id = :rental_a 
    AND EXISTS (SELECT 1 FROM rental WHERE rental_id = :rental_a);
    
    SELECT pg_sleep(0.001);
    
    UPDATE rental 
    SET last_update = NOW() 
    WHERE rental_id = :rental_b
    AND EXISTS (SELECT 1 FROM rental WHERE rental_id = :rental_b);

\else
    UPDATE customer 
    SET last_update = NOW(),
        active = active
    WHERE customer_id = :cliente_b;
    
    SELECT pg_sleep(0.002);
    
    UPDATE customer 
    SET last_update = NOW(),
        active = active
    WHERE customer_id = :cliente_a;
    
    UPDATE rental 
    SET last_update = NOW() 
    WHERE rental_id = :rental_b
    AND EXISTS (SELECT 1 FROM rental WHERE rental_id = :rental_b);
    
    SELECT pg_sleep(0.001);
    
    UPDATE rental 
    SET last_update = NOW() 
    WHERE rental_id = :rental_a
    AND EXISTS (SELECT 1 FROM rental WHERE rental_id = :rental_a);

\endif

INSERT INTO payment (customer_id, staff_id, rental_id, amount, payment_date)
VALUES (:cliente_a, 1, NULL, :monto_aleatorio, NOW());

COMMIT;
