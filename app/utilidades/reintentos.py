# Lógica de Reintentos para Fallos de Concurrencia
# TODO: Implementar decorador de reintentos con backoff exponencial
# TODO: Manejar fallos de deadlock y serialización
import time
from typing import Callable, TypeVar
from sqlalchemy import text
from sqlalchemy.engine import Connection
from sqlalchemy.exc import DBAPIError

T = TypeVar("T")
TX_ERRORS = {"40P01", "40001"}

def execute_isolated_tx(conn: Connection, func: Callable[[Connection], T], iso_level: str | None = None) -> T:
    tx = conn.begin()
    try:
        if iso_level:
            conn.execute(text(iso_level))
        res = func(conn)
        tx.commit()
        return res
    except Exception:
        tx.rollback()
        raise

def retry_tx(conn: Connection, func: Callable[[Connection], T], iso_level: str | None = None, max_tries: int = 5, backoff: float = 0.05) -> T:
    tries = 0
    while True:
        try:
            return execute_isolated_tx(conn, func, iso_level)
        except DBAPIError as e:
            origin = getattr(e, "orig", None)
            code = getattr(origin, "pgcode", None) or getattr(origin, "sqlstate", None)
            if code not in TX_ERRORS or tries >= max_tries:
                raise
            time.sleep(backoff * (2 ** tries))
            tries += 1