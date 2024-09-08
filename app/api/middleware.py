from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, Response
from typing import Callable, Awaitable
from core.config import settings
from db import SessionLocal, db_context

# CORS settings for the API
def cors_middleware(app: FastAPI) -> None:
    app.add_middleware(CORSMiddleware,
        allow_origins=settings.api_cors_origins,  # List of allowed origins
        allow_credentials=True,
        allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
        allow_headers=["*"],  # Allow all headers (Authorization, Content-Type, etc.)
    )

# Middleware to set the db in the context variable
class DBSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        with SessionLocal() as db:
            db_context.set(db)
            try:
                response = await call_next(request)
            except Exception as e:
                db.rollback()  # Ensure that any pending transactions are safely aborted
                raise e
            finally:
                db_context.set(None)
                db.close()
        return response

def db_session_middleware(app: FastAPI) -> None:
    app.add_middleware(DBSessionMiddleware)
