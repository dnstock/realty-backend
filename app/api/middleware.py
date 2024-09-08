from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, Response
from typing import Callable, Awaitable
from uuid import uuid4
from core import settings, request_id_context
from db import SessionLocal, db_session_context

# CORS settings for the API
def cors_middleware(app: FastAPI) -> None:
    app.add_middleware(CORSMiddleware,
        allow_origins=settings.api_cors_origins,  # List of allowed origins
        allow_credentials=True,
        allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
        allow_headers=["*"],  # Allow all headers (Authorization, Content-Type, etc.)
    )

# Middleware to add and handle request ID
class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        request_id = str(uuid4())
        request_id_context.set(request_id)
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id  # Return the request ID to the client
        return response

def request_id_middleware(app: FastAPI) -> None:
    app.add_middleware(RequestIDMiddleware)

# Middleware to manage the database session
class DBSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        with SessionLocal() as db:
            db_session_context.set(db)
            try:
                response = await call_next(request)
            except Exception as e:
                db.rollback()  # Rollback any pending transactions
                raise e
            finally:
                db_session_context.set(None)
                db.close()
        return response

def db_session_middleware(app: FastAPI) -> None:
    app.add_middleware(DBSessionMiddleware)
