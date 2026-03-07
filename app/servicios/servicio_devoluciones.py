from sqlalchemy import text
from sqlalchemy.engine import Connection
from app.esquemas import DevolucionRespuesta
from app.utilidades import api_error


def registrar_devolucion_read_committed(conn: Connection, rental_id: int) -> DevolucionRespuesta:
    query_seleccionar = text("SELECT rental_id, return_date FROM rental WHERE rental_id = :r_id FOR UPDATE")
    registro_actual = conn.execute(query_seleccionar, {"r_id": rental_id}).first()

    if not registro_actual:
        raise api_error(404, "RENTAL_NOT_FOUND", f"Renta {rental_id} no encontrada.")

    ya_devuelto = registro_actual.return_date is not None

    query_actualizar = text(
        "UPDATE rental SET return_date = COALESCE(return_date, NOW()) "
        "WHERE rental_id = :r_id RETURNING rental_id, return_date"
    )
    resultado = conn.execute(query_actualizar, {"r_id": rental_id}).one()

    mensaje = "Devolución registrada correctamente." if not ya_devuelto else "La renta ya había sido devuelta."

    return DevolucionRespuesta(
        rental_id=resultado.rental_id,
        return_date=resultado.return_date,
        mensaje=mensaje,
    )