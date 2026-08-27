from collections.abc import Callable
from time import perf_counter
from typing import Any

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from src.logg import logger


class LogAndErrorsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Any], Any]) -> Any:
        start_time = perf_counter()
        
        logger.info(
            f"На Входе {request.method} {request.path} | IP: {request.client_ip}"
        )
        
        try:
            response = call_next(request)
            process_time = (perf_counter() - start_time) * 1000
            logger.info(
                f"На выходе (Успех): {request.method} {request.path} | "
                f"Статус: {response.status_code} | Время: {process_time:.2f}ms"
            )
            return response 

        except StarletteHTTPException as exc:
            raise exc

        except Exception as exc:
            process_time = perf_counter() - start_time

            logger.exception(
                f"На выходе (Крит): {request.method} {request.path} | "
                f"Ошибка: {exc} | Время до падения: {process_time:2f}ms"
            )

            return JSONResponse(
                status_code=500,
                content={
                    "status": "error",
                    "message": "Ошибка на стороне сервера. Уже исправляем!"
                }
            )
