import logging

from src.celery_app.app import app
from src.database import Session
from src.vacancies.constants import PLATFORM_CODE
from src.vacancies.external_api.collect_vacancies import PlatformHH, PlatformVK
from src.vacancies.models import (
    AssociationTownPlatform,
    Platform,
    Town,
    Vacancy,
)

_logger = logging.getLogger(__name__)


@app.task
def collect_vacancies(platform_name):
    with Session() as session:
        platform = session.query(Platform).filter(Platform.name == platform_name)
        if not platform or not platform[0].url:
            _logger.error(f"Platform {platform_name} is not in the database")
            return
        platform = platform[0]
        towns = (
            session.query(Town.id, Town.name, AssociationTownPlatform.resource_id)
            .join(AssociationTownPlatform)
            .filter(AssociationTownPlatform.platform_id == platform.id)
        )

        if platform_name == PLATFORM_CODE.HH:
            platform_api = PlatformHH()
        elif platform_name == PLATFORM_CODE.VK:
            platform_api = PlatformVK()

        if not platform_api or not towns:
            _logger.error(f"Some problems in collect_vacancies")
            return

        session.query(Vacancy).filter(Vacancy.platform_id == platform.id).delete()
        for vacancies in platform_api.collect_vacancies(platform, towns):
            session.bulk_save_objects(vacancies)

        session.commit()
