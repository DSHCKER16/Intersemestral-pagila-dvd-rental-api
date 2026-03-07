from fastapi import APIRouter, status
from app.base_datos import get_connection
from app.esquemas import RentaCrear, RentaRespuesta
from app.servicios.servicio_rentas import crear_renta_serializable
from app.utilidades.transacciones import run_serializable_transaction

router = APIRouter()


@router.post("/", response_model=RentaRespuesta, status_code=status.HTTP_201_CREATED)
async def crear_renta(datos_renta: RentaCrear):
    with get_connection() as conn:
        resultado = run_serializable_transaction(
            conn, 
            lambda c: crear_renta_serializable(c, datos_renta)
        )
    return resultado