from sqlalchemy import text
from sqlalchemy.engine import Connection
from app.utilidades import api_error
from app.esquemas import PagoCrear, PagoRespuesta


def crear_pago_read_committed(conn: Connection, datos: PagoCrear) -> PagoRespuesta:
    dependencias = [
        ("customer", "customer_id", datos.customer_id),
        ("staff", "staff_id", datos.staff_id),
    ]
    for tabla, columna, valor in dependencias:
        if not conn.execute(text(f"SELECT 1 FROM {tabla} WHERE {columna} = :v"), {"v": valor}).first():
            raise api_error(404, f"{tabla.upper()}_NOT_FOUND", f"{tabla.capitalize()} con id {valor} no encontrado.")

    rental_id = datos.rental_id
    if rental_id:
        registro_renta = conn.execute(
            text("SELECT rental_id, customer_id FROM rental WHERE rental_id = :id"), 
            {"id": rental_id}
        ).first()
        if not registro_renta:
            raise api_error(404, "RENTAL_NOT_FOUND", f"Renta id {rental_id} no existe.")
        if registro_renta.customer_id != datos.customer_id:
            raise api_error(400, "RENTAL_CUSTOMER_MISMATCH", "El rental_id no corresponde al customer_id.")

    query_insertar = text(
        "INSERT INTO payment (customer_id, staff_id, rental_id, amount, payment_date) "
        "VALUES (:c, :s, :r, :a, NOW()) "
        "RETURNING payment_id, customer_id, staff_id, rental_id, amount, payment_date"
    )
    nuevo_pago = conn.execute(
        query_insertar, 
        {"c": datos.customer_id, "s": datos.staff_id, "r": rental_id, "a": datos.amount}
    ).one()

    return PagoRespuesta(
        payment_id=nuevo_pago.payment_id,
        customer_id=nuevo_pago.customer_id,
        staff_id=nuevo_pago.staff_id,
        rental_id=nuevo_pago.rental_id,
        amount=nuevo_pago.amount,
        payment_date=nuevo_pago.payment_date,
    )