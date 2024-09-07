from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
from core.logger import log_exception

def common_http_exception_handler(app: FastAPI) -> None:
    def handler(request: Request, exc: HTTPException) -> JSONResponse:
        log_exception(request, exc)
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )
    app.add_exception_handler(HTTPException, handler) # type: ignore (only HTTPException is allowed)

def common_validation_exception_handler(app: FastAPI) -> None:
    def handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        log_exception(request, exc)
        return JSONResponse(
            status_code=422,
            content={"detail": exc.errors(), "body": exc.body},
        )
    app.add_exception_handler(RequestValidationError, handler) # type: ignore (only RequestValidationError is allowed)

def common_sqlalchemy_exception_handler(app: FastAPI) -> None:
    def handler(request: Request, exc: IntegrityError) -> JSONResponse:
        log_exception(request, exc)
        return JSONResponse(
            status_code=400,
            content={"detail": "Database integrity error occurred."},
        )
    app.add_exception_handler(IntegrityError, handler) # type: ignore (only IntegrityError is allowed)

def common_unhandled_exception_handler(app: FastAPI) -> None:
    def handler(request: Request, exc: Exception) -> JSONResponse:
        log_exception(request, exc)
        return JSONResponse(
            status_code=500,
            content={"detail": "An unexpected server error occurred."},
        )
    app.add_exception_handler(Exception, handler)
