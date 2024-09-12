from starlette.datastructures import FormData
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
from core.logger import log_middleware_exception

def common_http_exception_handler(app: FastAPI) -> None:
    def handler(request: Request, exc: HTTPException) -> JSONResponse:
        log_middleware_exception(exc, request)
        return JSONResponse(
            status_code=exc.status_code,
            content={'detail': exc.detail},
        )
    app.add_exception_handler(HTTPException, handler) # type: ignore (only HTTPException is allowed)

def common_validation_exception_handler(app: FastAPI) -> None:
    def handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        log_middleware_exception(exc, request)
        body = exc.body
        if isinstance(body, FormData):
            body = dict(body)  # Convert FormData to a dictionary (serializable)
        elif isinstance(body, (dict, list)):
            pass  # Already serializable
        elif isinstance(body, (str, bytes)):
            body = {'raw_body': body}  # Wrap raw data in a dictionary to make it serializable
        else:
            body = None  # Fallback in case body type is unexpected or unhandled
        return JSONResponse(
            status_code=422,
            content={'detail': exc.errors(), 'body': body},
        )
    app.add_exception_handler(RequestValidationError, handler) # type: ignore (only RequestValidationError is allowed)

def common_sqlalchemy_exception_handler(app: FastAPI) -> None:
    def handler(request: Request, exc: IntegrityError) -> JSONResponse:
        log_middleware_exception(exc, request)
        return JSONResponse(
            status_code=400,
            content={'detail': 'Database integrity error occurred.'},
        )
    app.add_exception_handler(IntegrityError, handler) # type: ignore (only IntegrityError is allowed)

def common_unhandled_exception_handler(app: FastAPI) -> None:
    def handler(request: Request, exc: Exception) -> JSONResponse:
        log_middleware_exception(exc, request)
        return JSONResponse(
            status_code=500,
            content={'detail': 'An unexpected server error occurred.'},
        )
    app.add_exception_handler(Exception, handler)
