from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.base_datos import obtener_db
from app.esquemas import RentalCrear, RentalRespuesta, ErrorRespuesta
from app.modelos import Rental
from typing import List

router = APIRouter()


@router.post("/", response_model=RentalRespuesta, status_code=status.HTTP_201_CREATED)
async def crear_renta(
    rental_data: RentalCrear,
    db: Session = Depends(obtener_db)
):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Endpoint en implementación"
    )


@router.get("/", response_model=List[RentalRespuesta], status_code=status.HTTP_200_OK)
async def listar_rentas(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(obtener_db)
):
    rentas = db.query(Rental).offset(skip).limit(limit).all()
    return rentas