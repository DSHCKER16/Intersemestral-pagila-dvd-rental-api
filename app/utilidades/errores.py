from fastapi import HTTPException


def api_error(codigo_estado: int, codigo_error: str, detalle: str) -> HTTPException:
    return HTTPException(
        status_code=codigo_estado,
        detail={"codigo_error": codigo_error, "mensaje": detalle}
    )
