from app.configuracion import obtener_configuracion
from app.rutas import rentas, devoluciones, pagos

config = obtener_configuracion()

app = FastAPI(
    title="Pagila DVD Rental API",
    description="API REST para sistema de renta de películas - Proyecto Intersemestral",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rentas.router, prefix="/rentals", tags=["Rentas"])
app.include_router(devoluciones.router, prefix="/returns", tags=["Devoluciones"])
app.include_router(pagos.router, prefix="/payments", tags=["Pagos"])


@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {
        "mensaje": "Pagila DVD Rental API - Proyecto Intersemestral",
        "version": "1.0.0",
        "documentacion": "/docs"
    }


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {
        "status": "ok",
        "servicio": "Pagila DVD Rental API"
    }
