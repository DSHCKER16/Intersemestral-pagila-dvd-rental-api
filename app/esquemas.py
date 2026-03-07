from datetime import datetime
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict


class RentaCrear(BaseModel):
    customer_id: int = Field(gt=0, description="ID del cliente")
    inventory_id: int = Field(gt=0, description="ID del inventario")
    staff_id: int = Field(gt=0, description="ID del staff")


class RentaRespuesta(BaseModel):
    rental_id: int
    rental_date: datetime
    inventory_id: int
    customer_id: int
    staff_id: int
    
    model_config = ConfigDict(from_attributes=True)


class DevolucionRespuesta(BaseModel):
    rental_id: int
    return_date: datetime
    mensaje: str
    
    model_config = ConfigDict(from_attributes=True)


class PagoCrear(BaseModel):
    customer_id: int = Field(gt=0, description="ID del cliente")
    staff_id: int = Field(gt=0, description="ID del staff")
    amount: Decimal = Field(gt=0, description="Monto del pago")
    rental_id: Optional[int] = Field(default=None, gt=0, description="ID de la renta (opcional)")


class PagoRespuesta(BaseModel):
    payment_id: int
    customer_id: int
    staff_id: int
    rental_id: Optional[int] = None
    amount: Decimal
    payment_date: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ErrorRespuesta(BaseModel):
    detalle: str
    codigo_error: Optional[str] = None
