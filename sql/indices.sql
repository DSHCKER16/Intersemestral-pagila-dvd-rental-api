CREATE INDEX IF NOT EXISTS idx_rental_return_date ON rental(return_date);

CREATE INDEX IF NOT EXISTS idx_rental_activas ON rental(inventory_id) WHERE return_date IS NULL;

CREATE INDEX IF NOT EXISTS idx_rental_customer_date ON rental(customer_id, rental_date);

CREATE INDEX IF NOT EXISTS idx_rental_inventory_return ON rental(inventory_id, return_date);

CREATE INDEX IF NOT EXISTS idx_payment_customer_date ON payment(customer_id, payment_date);

CREATE INDEX IF NOT EXISTS idx_payment_date ON payment(payment_date);

CREATE INDEX IF NOT EXISTS idx_payment_amount ON payment(amount) WHERE amount > 10;

CREATE INDEX IF NOT EXISTS idx_inventory_store_film ON inventory(store_id, film_id);

CREATE INDEX IF NOT EXISTS idx_film_category ON film_category(category_id, film_id);

CREATE INDEX IF NOT EXISTS idx_customer_active ON customer(customer_id) WHERE active = 1;