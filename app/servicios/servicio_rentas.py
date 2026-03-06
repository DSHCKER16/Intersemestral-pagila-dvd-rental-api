from sqlalchemy import text
from sqlalchemy.engine import Connection
from sqlalchemy.exc import IntegrityError
from app.errores import api_error
from app.esquemas import RentalCreate, RentalResponse

def create_rental_serializable(conn: Connection, payload: RentalCreate) -> RentalResponse:
    checks = [
        ("customer", "customer_id", payload.customer_id),
        ("inventory", "inventory_id", payload.inventory_id),
        ("staff", "staff_id", payload.staff_id),
    ]
    for t, c, v in checks:
        if not conn.execute(text(f"SELECT 1 FROM {t} WHERE {c} = :val"), {"val": v}).first():
            raise api_error(404, f"{t.upper()}_NOT_FOUND", f"{t.capitalize()} id {v} no existe.")

    try:
        q = text("INSERT INTO rental (rental_date, inventory_id, customer_id, return_date, staff_id) VALUES (NOW(), :i, :c, NULL, :s) RETURNING rental_id, rental_date, inventory_id, customer_id, staff_id")
        record = conn.execute(q, {"i": payload.inventory_id, "c": payload.customer_id, "s": payload.staff_id}).one()
    except IntegrityError as e:
        orig = getattr(e, "orig", None)
        code = getattr(orig, "pgcode", None) or getattr(orig, "sqlstate", None)
        if code == "23505":
            raise api_error(409, "RENTAL_ALREADY_ACTIVE", "El inventory_id ya está rentado.")
        raise

    return RentalResponse(
        rental_id=record.rental_id,
        rental_date=record.rental_date,
        inventory_id=record.inventory_id,
        customer_id=record.customer_id,
        staff_id=record.staff_id,
    )