from sqlalchemy import text
from sqlalchemy.engine import Connection
from app.esquemas import ReturnResponse
from app.utilidades import api_error

def registrar_devolucion_read_committed(conn: Connection, rental_id: int) -> ReturnResponse:
    q_sel = text("SELECT rental_id, return_date FROM rental WHERE rental_id = :r_id FOR UPDATE")
    registro_actual = conn.execute(q_sel, {"r_id": rental_id}).first()

    if not registro_actual:
        raise api_error(404, "RENTAL_NOT_FOUND", f"Renta {rental_id} no encontrada.")

    ya_devuelto = registro_actual.return_date is not None

    q_upd = text("UPDATE rental SET return_date = COALESCE(return_date, NOW()) WHERE rental_id = :r_id RETURNING rental_id, return_date")
    resultado = conn.execute(q_upd, {"r_id": rental_id}).one()

    return ReturnResponse(
        rental_id=resultado.rental_id,
        return_date=resultado.return_date,
        already_returned=ya_devuelto,
    )