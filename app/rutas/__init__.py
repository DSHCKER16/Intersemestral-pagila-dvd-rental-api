# Paquete de Rutas de la API
from .rentas import router as router_rentas
from .devoluciones import router as router_devoluciones
from .pagos import router as router_pagos

__all__ = [
    "router_rentas",
    "router_devoluciones",
    "router_pagos",
]
