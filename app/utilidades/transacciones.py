
from typing import Callable, TypeVar
from sqlalchemy.engine import Connection
from app.utilidades.reintentos import retry_tx

T = TypeVar("T")

def run_serializable_transaction(conn: Connection, func: Callable[[Connection], T]) -> T:
    return retry_tx(conn, func, "SET LOCAL TRANSACTION ISOLATION LEVEL SERIALIZABLE")

def run_read_committed_transaction(conn: Connection, func: Callable[[Connection], T]) -> T:
    return retry_tx(conn, func, "SET LOCAL TRANSACTION ISOLATION LEVEL READ COMMITTED")