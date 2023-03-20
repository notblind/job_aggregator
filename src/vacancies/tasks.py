import logging

from requests.exceptions import HTTPError

from src.celery_app.app import app
from src.database import Session
from src.vacancies.constants import PLATFORM_CODES
from src.vacancies.models import (AssociationTownPlatform, Platform, Town,
                                  Vacancy)
from src.vacancies.platform_api import (collect_vacancies_from_hh,
                                        collect_vacancies_from_vk)

_logger = logging.getLogger(__name__)


@app.task
def collect_vacancies(platform_name):
    with Session() as session:
        platform = session.query(Platform).filter(Platform.name == platform_name)
        if not platform or not platform[0].url:
            _logger.error(f'Platform {platform_name} is not in the database')
            return
        platform = platform[0]
        towns = session.query(
            Town.id,
            Town.name,
            AssociationTownPlatform.resource_id
        ).join(
            AssociationTownPlatform
        ).filter(
            AssociationTownPlatform.platform_id == platform.id
        )

        try:
            if platform_name == PLATFORM_CODES.HH:
                objects = collect_vacancies_from_hh(platform, towns)
            elif platform_name == PLATFORM_CODES.VK:
                objects = collect_vacancies_from_vk(platform, towns)
            else:
                objects = []
        except HTTPError as e:
            _logger.error(
                f"HTTPError: {e}"
            )
            return
        except Exception as e:
            _logger.error(f'Error occurred while collect vacancies from {platform_name}: {e}')
            return

        if objects:
            session.query(Vacancy).filter(Vacancy.platform_id == platform.id).delete()
            session.bulk_save_objects(objects)
            session.commit()
