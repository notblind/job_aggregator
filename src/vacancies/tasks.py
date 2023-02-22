import logging

from src.celery_app.app import app


_logger = logging.getLogger(__name__)


@app.task
def collect_vacancies_from_hh():
    _logger.error('celery test')
