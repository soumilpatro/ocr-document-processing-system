from datetime import datetime, UTC
from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        exc: HTTPException,
    ):

        status_name = HTTPStatus(exc.status_code).phrase

        if isinstance(exc.detail, dict):

            return JSONResponse(

                status_code=exc.status_code,

                content={

                    "statusCode": exc.status_code,

                    "status": status_name,

                    "errorCode": exc.detail.get("errorCode"),

                    "message": exc.detail.get("message"),

                    "timestamp": datetime.now(UTC).isoformat()

                }

            )

        return JSONResponse(

            status_code=exc.status_code,

            content={

                "statusCode": exc.status_code,

                "status": status_name,

                "errorCode": "HTTP_ERROR",

                "message": str(exc.detail),

                "timestamp": datetime.now(UTC).isoformat()

            }

        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request,
        exc: Exception,
    ):

        return JSONResponse(

            status_code=500,

            content={

                "statusCode": 500,

                "status": HTTPStatus(500).phrase,

                "errorCode": "INTERNAL_SERVER_ERROR",

                "message": "An unexpected error occurred.",

                "timestamp": datetime.now(UTC).isoformat()

            }

        )