from fastapi import FastAPI

from src.vacancies.router import router as router_vacancies

app = FastAPI(
    title='Vacancies',
    version='0.0.1',
)

app.include_router(router_vacancies)
