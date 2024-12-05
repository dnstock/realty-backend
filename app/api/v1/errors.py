#
# Description: Custom error handlers for API v1 exclusively
#
# For global or general error handlers see: backend/app/api/errors.py
#
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from core.logger import log_middleware_exception

# Custom handler for HTTPException specific to v1
def v1_http_exception_handler(app: FastAPI) -> None:
    def handler(request: Request, exc: HTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={'detail (v1-specific)': exc.detail},
        )
    app.add_exception_handler(HTTPException, handler) # type: ignore (only HTTPException is allowed)

# Custom handler for unhandled exceptions specific to v1
def v1_unhandled_exception_handler(app: FastAPI) -> None:
    def handler(request: Request, exc: Exception) -> JSONResponse:
        log_middleware_exception(exc, request)
        return JSONResponse(
            status_code=500,
            content={'detail (v1-specific)': 'An unexpected server error occurred.'},
        )
    app.add_exception_handler(Exception, handler)
