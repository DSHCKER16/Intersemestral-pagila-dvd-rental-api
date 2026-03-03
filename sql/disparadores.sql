CREATE TABLE IF NOT EXISTS registro_auditoria (
    id SERIAL PRIMARY KEY,
    fecha_evento TIMESTAMP DEFAULT NOW(),
    nombre_tabla VARCHAR(50),
    operacion VARCHAR(10),
    valor_pk INTEGER,
    fila_anterior JSONB,
    fila_nueva JSONB
);

CREATE OR REPLACE FUNCTION fn_trigger_auditoria()
RETURNS TRIGGER AS $$
DECLARE
    valor_pk INTEGER;
    json_anterior JSONB;
    json_nuevo JSONB;
BEGIN
    IF TG_OP = 'DELETE' THEN
        valor_pk := OLD.rental_id;
        json_anterior := row_to_json(OLD)::JSONB;
        json_nuevo := NULL;
    ELSIF TG_OP = 'UPDATE' THEN
        IF TG_TABLE_NAME = 'rental' THEN
            valor_pk := NEW.rental_id;
        ELSIF TG_TABLE_NAME = 'payment' THEN
            valor_pk := NEW.payment_id;
        END IF;
        json_anterior := row_to_json(OLD)::JSONB;
        json_nuevo := row_to_json(NEW)::JSONB;
    ELSIF TG_OP = 'INSERT' THEN
        IF TG_TABLE_NAME = 'rental' THEN
            valor_pk := NEW.rental_id;
        ELSIF TG_TABLE_NAME = 'payment' THEN
            valor_pk := NEW.payment_id;
        END IF;
        json_anterior := NULL;
        json_nuevo := row_to_json(NEW)::JSONB;
    END IF;

    INSERT INTO registro_auditoria (nombre_tabla, operacion, valor_pk, fila_anterior, fila_nueva)
    VALUES (TG_TABLE_NAME, TG_OP, valor_pk, json_anterior, json_nuevo);

    IF TG_OP = 'DELETE' THEN
        RETURN OLD;
    ELSE
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_auditoria_rental ON rental;
CREATE TRIGGER trg_auditoria_rental
AFTER INSERT OR UPDATE OR DELETE ON rental
FOR EACH ROW EXECUTE FUNCTION fn_trigger_auditoria();

DROP TRIGGER IF EXISTS trg_auditoria_payment ON payment;
CREATE TRIGGER trg_auditoria_payment
AFTER INSERT OR UPDATE OR DELETE ON payment
FOR EACH ROW EXECUTE FUNCTION fn_trigger_auditoria();

CREATE OR REPLACE FUNCTION fn_validar_rentas_vencidas()
RETURNS TRIGGER AS $$
DECLARE
    rentas_vencidas INTEGER;
BEGIN
    SELECT COUNT(*) INTO rentas_vencidas
    FROM rental
    WHERE customer_id = NEW.customer_id
      AND return_date IS NULL
      AND rental_date + INTERVAL '7 days' < NOW();

    IF rentas_vencidas > 0 THEN
        RAISE EXCEPTION 'Cliente tiene % rentas vencidas sin devolver', rentas_vencidas;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_validar_rentas_vencidas ON rental;
CREATE TRIGGER trg_validar_rentas_vencidas
BEFORE INSERT ON rental
FOR EACH ROW EXECUTE FUNCTION fn_validar_rentas_vencidas();