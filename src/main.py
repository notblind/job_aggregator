from celery import Celery
from fastapi import FastAPI

import settings


app = FastAPI(
    title='Vacancies',
    version='0.0.1',
)

celery = Celery(
    __name__,
    broker=f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}',
    backend=f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}',
)

celery.conf.imports = [
    'vacancies.tasks'
]
