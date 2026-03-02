from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.base_datos import obtener_db
from app.esquemas import DevolucionRespuesta, ErrorRespuesta
from app.modelos import Rental

router = APIRouter()


@router.post("/{rental_id}", response_model=DevolucionRespuesta, status_code=status.HTTP_200_OK)
async def registrar_devolucion(
    rental_id: int,
    db: Session = Depends(obtener_db)
):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Endpoint en implementación"
    )
