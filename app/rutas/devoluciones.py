from fastapi import APIRouter, status
from app.base_datos import get_connection
from app.esquemas import DevolucionRespuesta
from app.servicios.servicio_devoluciones import registrar_devolucion_read_committed
from app.utilidades.transacciones import run_read_committed_transaction

router = APIRouter()


@router.post("/{rental_id}", response_model=DevolucionRespuesta, status_code=status.HTTP_200_OK)
async def registrar_devolucion(rental_id: int):
    with get_connection() as conn:
        resultado = run_read_committed_transaction(
            conn, 
            lambda c: registrar_devolucion_read_committed(c, rental_id)
        )
    return resultado