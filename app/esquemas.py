from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional
from decimal import Decimal


class RentalCrear(BaseModel):
    customer_id: int = Field(..., gt=0, description="ID del cliente")
    inventory_id: int = Field(..., gt=0, description="ID del inventario")
    staff_id: int = Field(..., gt=0, description="ID del staff")


class RentalRespuesta(BaseModel):
    rental_id: int
    rental_date: datetime
    inventory_id: int
    customer_id: int
    return_date: Optional[datetime] = None
    staff_id: int
    last_update: datetime
    
    model_config = ConfigDict(from_attributes=True)


class DevolucionRespuesta(BaseModel):
    rental_id: int
    return_date: datetime
    mensaje: str
    
    model_config = ConfigDict(from_attributes=True)


class PagoCrear(BaseModel):
    customer_id: int = Field(..., gt=0, description="ID del cliente")
    staff_id: int = Field(..., gt=0, description="ID del staff")
    amount: Decimal = Field(..., gt=0, description="Monto del pago")
    rental_id: Optional[int] = Field(None, gt=0, description="ID de la renta (opcional)")


class PagoRespuesta(BaseModel):
    payment_id: int
    customer_id: int
    staff_id: int
    rental_id: Optional[int] = None
    amount: Decimal
    payment_date: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ErrorRespuesta(BaseModel):
    detail: str
    error_code: Optional[str] = None


class MensajeRespuesta(BaseModel):
    mensaje: str
    datos: Optional[dict] = None

    from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class RentalCreate(BaseModel):
    customer_id: int = Field(gt=0)
    inventory_id: int = Field(gt=0)
    staff_id: int = Field(gt=0)

class RentalResponse(BaseModel):
    rental_id: int
    customer_id: int
    inventory_id: int
    staff_id: int
    rental_date: datetime
    model_config = ConfigDict(from_attributes=True)

class ReturnResponse(BaseModel):
    rental_id: int
    return_date: datetime
    already_returned: bool

class PaymentCreate(BaseModel):
    customer_id: int = Field(gt=0)
    staff_id: int = Field(gt=0)
    amount: float = Field(gt=0)
    rental_id: Optional[int] = Field(default=None, gt=0)

class PaymentResponse(BaseModel):
    payment_id: int
    customer_id: int
    staff_id: int
    rental_id: Optional[int]
    amount: float
    payment_date: datetime
    model_config = ConfigDict(from_attributes=True)
