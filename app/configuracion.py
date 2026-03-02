from pydantic_settings import BaseSettings
from functools import lru_cache


class Configuracion(BaseSettings):
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str = "pagila"
    DATABASE_USER: str = "postgres"
    DATABASE_PASSWORD: str = "postgres"
    
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    
    @property
    def database_url(self) -> str:
        return f"postgresql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def obtener_configuracion() -> Configuracion:
    return Configuracion()
