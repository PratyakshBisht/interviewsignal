from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import time
from typing import Callable
import logging

logger = logging.getLogger(__name__)


def setup_security_middleware(app):
    """Configure all security middleware."""

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://localhost:3000",
            "https://interviewsignal.app",
            "https://*.interviewsignal.app",
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=[
            "Content-Type",
            "Authorization",
            "X-Requested-With",
            "X-CSRF-Token",
            "X-API-Key",
        ],
        expose_headers=["X-Total-Count", "Content-Range", "X-Process-Time"],
        max_age=600,
    )

    # Trusted hosts
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=[
            "localhost",
            "127.0.0.1",
            "0.0.0.0",
            "interviewsignal.app",
            "api.interviewsignal.app",
            "*.interviewsignal.app",
        ],
    )

    # GZip compression
    app.add_middleware(GZipMiddleware, minimum_size=1000)

    # Request logging & process time middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next: Callable):
        start_time = time.time()
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000

        if request.url.path not in ["/health", "/metrics"]:
            logger.info(
                f"{request.method} {request.url.path} "
                f"Status: {response.status_code} "
                f"Duration: {process_time:.2f}ms "
                f"IP: {request.client.host if request.client else 'unknown'}"
            )

        response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
        return response

    # Security headers middleware
    @app.middleware("http")
    async def add_security_headers(request: Request, call_next: Callable):
        response = await call_next(request)

        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"

        return response

    return app
