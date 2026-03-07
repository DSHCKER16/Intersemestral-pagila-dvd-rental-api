import time
from typing import Callable, TypeVar
from sqlalchemy import text
from sqlalchemy.engine import Connection
from sqlalchemy.exc import DBAPIError

T = TypeVar("T")
CODIGOS_ERROR_TX = {"40P01", "40001"}


def execute_isolated_tx(conn: Connection, func: Callable[[Connection], T], nivel_aislamiento: str | None = None) -> T:
    tx = conn.begin()
    try:
        if nivel_aislamiento:
            conn.execute(text(nivel_aislamiento))
        resultado = func(conn)
        tx.commit()
        return resultado
    except Exception:
        tx.rollback()
        raise


def retry_tx(
    conn: Connection, 
    func: Callable[[Connection], T], 
    nivel_aislamiento: str | None = None, 
    max_intentos: int = 5, 
    backoff: float = 0.05
) -> T:
    intentos = 0
    while True:
        try:
            return execute_isolated_tx(conn, func, nivel_aislamiento)
        except DBAPIError as e:
            origen = getattr(e, "orig", None)
            codigo = getattr(origen, "pgcode", None) or getattr(origen, "sqlstate", None)
            
            if codigo not in CODIGOS_ERROR_TX or intentos >= max_intentos:
                raise
            
            tiempo_espera = backoff * (2 ** intentos)
            time.sleep(tiempo_espera)
            intentos += 1