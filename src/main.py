from fastapi import FastAPI

from src.common.httpx_client import client_httpx_start, client_httpx_stop
from src.vacancies.router import router as router_vacancies

app = FastAPI(
    title='Vacancies',
    version='0.0.1',
    on_startup=[client_httpx_start],
    on_shutdown=[client_httpx_stop],
)

app.include_router(router_vacancies)
