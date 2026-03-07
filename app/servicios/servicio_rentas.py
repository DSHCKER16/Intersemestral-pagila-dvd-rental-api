from sqlalchemy import text
from sqlalchemy.engine import Connection
from sqlalchemy.exc import IntegrityError
from app.utilidades import api_error
from app.esquemas import RentaCrear, RentaRespuesta


def crear_renta_serializable(conn: Connection, datos: RentaCrear) -> RentaRespuesta:
    validaciones = [
        ("customer", "customer_id", datos.customer_id),
        ("inventory", "inventory_id", datos.inventory_id),
        ("staff", "staff_id", datos.staff_id),
    ]
    for tabla, columna, valor in validaciones:
        existe = conn.execute(
            text(f"SELECT 1 FROM {tabla} WHERE {columna} = :val"), 
            {"val": valor}
        ).first()
        if not existe:
            raise api_error(404, f"{tabla.upper()}_NOT_FOUND", f"{tabla.capitalize()} con id {valor} no existe.")

    disponible = conn.execute(
        text(
            "SELECT 1 FROM inventory WHERE inventory_id = :inv "
            "AND NOT EXISTS (SELECT 1 FROM rental WHERE inventory_id = :inv AND return_date IS NULL)"
        ),
        {"inv": datos.inventory_id}
    ).first()
    
    if not disponible:
        raise api_error(409, "INVENTORY_NOT_AVAILABLE", f"Inventory {datos.inventory_id} no está disponible.")

    try:
        query = text(
            "INSERT INTO rental (rental_date, inventory_id, customer_id, return_date, staff_id) "
            "VALUES (NOW(), :i, :c, NULL, :s) "
            "RETURNING rental_id, rental_date, inventory_id, customer_id, staff_id"
        )
        registro = conn.execute(
            query, 
            {"i": datos.inventory_id, "c": datos.customer_id, "s": datos.staff_id}
        ).one()
    except IntegrityError as e:
        origen = getattr(e, "orig", None)
        codigo = getattr(origen, "pgcode", None) or getattr(origen, "sqlstate", None)
        if codigo == "23505":
            raise api_error(409, "RENTAL_ALREADY_ACTIVE", "El inventory_id ya está rentado por otro cliente.")
        raise

    return RentaRespuesta(
        rental_id=registro.rental_id,
        rental_date=registro.rental_date,
        inventory_id=registro.inventory_id,
        customer_id=registro.customer_id,
        staff_id=registro.staff_id,
    )