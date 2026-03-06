from fastapi import APIRouter, status
from app.base_datos import get_connection
from app.esquemas import DevolucionRespuesta
from app.servicios.servicio_devoluciones import registrar_devolucion_read_committed

router = APIRouter()


@router.post("/{rental_id}", response_model=DevolucionRespuesta, status_code=status.HTTP_200_OK)
async def registrar_devolucion(rental_id: int):
    with get_connection() as conn:
        resultado = registrar_devolucion_read_committed(conn, rental_id)

    mensaje = "Devolución registrada." if not resultado.already_returned else "La renta ya había sido devuelta."
    return DevolucionRespuesta(
        rental_id=resultado.rental_id,
        return_date=resultado.return_date,
        mensaje=mensaje,
    )