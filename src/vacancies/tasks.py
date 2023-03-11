import logging
import requests
from requests.exceptions import HTTPError

from src.settings import HH_URL
from src.celery_app.app import app


_logger = logging.getLogger(__name__)


@app.task
def collect_vacancies_from_hh():
    try:
        requests.get(HH_URL)
    except HTTPError as e:
        _logger.error(
            f"HTTP error occurred while collect vacancies from hh: {e}"
        )
    except Exception as err:
        _logger.error(f"Error occurred while collect vacancies from hh: {err}")

    _logger.error("celery test")
