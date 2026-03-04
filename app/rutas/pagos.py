from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.base_datos import obtener_db
from app.esquemas import PagoCrear, PagoRespuesta, ErrorRespuesta
from app.modelos import Payment
from typing import List

router = APIRouter()


@router.post("/", response_model=PagoRespuesta, status_code=status.HTTP_201_CREATED)
async def crear_pago(
    pago_data: PagoCrear,
    db: Session = Depends(obtener_db)
):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Endpoint en implementación"
    )


@router.get("/", response_model=List[PagoRespuesta], status_code=status.HTTP_200_OK)
async def listar_pagos(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(obtener_db)
):
    pagos = db.query(Payment).offset(skip).limit(limit).all()
    return pagos