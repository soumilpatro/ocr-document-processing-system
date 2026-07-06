from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        exc: HTTPException,
    ):

        if isinstance(exc.detail, dict):

            return JSONResponse(

                status_code=exc.status_code,

                content={

                    "errorCode": exc.detail.get("errorCode"),

                    "message": exc.detail.get("message"),

                    "timestamp": datetime.utcnow().isoformat()

                }

            )

        return JSONResponse(

            status_code=exc.status_code,

            content={

                "errorCode": "HTTP_ERROR",

                "message": str(exc.detail),

                "timestamp": datetime.utcnow().isoformat()

            }

        )