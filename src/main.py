from celery import Celery
from fastapi import FastAPI

from src.settings import REDIS_HOST, REDIS_PORT, REDIS_DB


app = FastAPI(
    title='Vacancies',
    version='0.0.1',
)

celery_app = Celery(
    __name__,
    broker=f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}',
    backend=f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}',
)
