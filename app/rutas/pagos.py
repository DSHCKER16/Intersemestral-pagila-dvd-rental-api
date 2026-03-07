from fastapi import APIRouter, status
from app.base_datos import get_connection
from app.esquemas import PagoCrear, PagoRespuesta
from app.servicios.servicio_pagos import crear_pago_read_committed
from app.utilidades.transacciones import run_read_committed_transaction

router = APIRouter()


@router.post("/", response_model=PagoRespuesta, status_code=status.HTTP_201_CREATED)
async def crear_pago(datos_pago: PagoCrear):
    with get_connection() as conn:
        resultado = run_read_committed_transaction(
            conn, 
            lambda c: crear_pago_read_committed(c, datos_pago)
        )
    return resultado