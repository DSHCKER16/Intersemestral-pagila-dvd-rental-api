\set cliente_a random(1, 299)
\set cliente_b random(300, 599)
\set monto_aleatorio random(1, 10)

BEGIN;

UPDATE customer SET last_update = NOW() WHERE customer_id = :cliente_a;

SELECT pg_sleep(0.001);

UPDATE customer SET last_update = NOW() WHERE customer_id = :cliente_b;

INSERT INTO payment (customer_id, staff_id, rental_id, amount, payment_date)
VALUES (:cliente_a, 1, NULL, :monto_aleatorio, NOW());

COMMIT;
