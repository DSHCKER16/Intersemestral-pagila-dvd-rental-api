from sqlalchemy import text
from sqlalchemy.engine import Connection
from app.utilidades import api_error
from app.esquemas import PaymentCreate, PaymentResponse

def create_payment_read_committed(conn: Connection, payload: PaymentCreate) -> PaymentResponse:
    dependencies = [
        ("customer", "customer_id", payload.customer_id),
        ("staff", "staff_id", payload.staff_id),
    ]
    for tbl, col, val in dependencies:
        if not conn.execute(text(f"SELECT 1 FROM {tbl} WHERE {col} = :v"), {"v": val}).first():
            raise api_error(404, f"{tbl.upper()}_NOT_FOUND", f"{tbl.capitalize()} con id {val} no encontrado.")

    r_id = payload.rental_id
    if r_id:
        r_record = conn.execute(text("SELECT rental_id, customer_id FROM rental WHERE rental_id = :id"), {"id": r_id}).first()
        if not r_record:
            raise api_error(404, "RENTAL_NOT_FOUND", f"Renta id {r_id} no existe.")
        if r_record.customer_id != payload.customer_id:
            raise api_error(400, "RENTAL_CUSTOMER_MISMATCH", "El rental_id no corresponde al customer_id.")

    ins_query = text("INSERT INTO payment (customer_id, staff_id, rental_id, amount, payment_date) VALUES (:c, :s, :r, :a, NOW()) RETURNING payment_id, customer_id, staff_id, rental_id, amount, payment_date")
    new_payment = conn.execute(ins_query, {"c": payload.customer_id, "s": payload.staff_id, "r": r_id, "a": payload.amount}).one()

    return PaymentResponse(
        payment_id=new_payment.payment_id,
        customer_id=new_payment.customer_id,
        staff_id=new_payment.staff_id,
        rental_id=new_payment.rental_id,
        amount=new_payment.amount,
        payment_date=new_payment.payment_date,
    )