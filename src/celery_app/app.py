from celery import Celery

from src.celery_app import config
from src.settings import REDIS_HOST, REDIS_PORT, REDIS_DB

app = Celery(
    'vacancies',
    broker=f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}',
    backend=f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}',
)

app.config_from_object(config)
