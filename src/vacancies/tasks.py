import logging
import requests
from datetime import datetime, timedelta
from requests.exceptions import HTTPError

from fastapi import status
from pydantic import ValidationError

from src.settings import HH_URL
from src.celery_app.app import app
from src.database import Session
from src.vacancies.models import Platform, Vacancy, Town
from src.vacancies.pydantic_models import PydanticVacancy

_logger = logging.getLogger(__name__)


@app.task
def collect_vacancies_from_hh():
    with Session() as session:
        page = 0
        params = {
            'per_page': 100,
            'page': page,
            'date_from': (datetime.utcnow() - timedelta(days=30)).strftime('%Y-%m-%d')
        }
        objects = []

        platform = session.query(Platform).filter(Platform.name == 'hh')
        if not platform:
            _logger.error('No hh platform')
            return
        platform = platform[0]
        towns = session.query(Town)

        try:
            while page < 100:
                response = requests.get(HH_URL, params=params)
                if response.status_code == status.HTTP_200_OK:
                    items = response.json().get('items')
                    for item in items:
                        try:
                            address = item.get('address') if item.get('address') else {}
                            salary = item.get('salary') if item.get('salary') else {}
                            snippet = item.get('snippet') if item.get('snippet') else {}
                            town = (item.get('area') if item.get('area') else {}).get('name')
                            if town:
                                filter_towns = [db_town for db_town in towns if town == db_town.name]
                                _logger.error(filter_towns)
                                if filter_towns:
                                    town = filter_towns[0]
                                else:
                                    town = Town(name=town)
                                    session.add(town)
                                    session.flush()
                            vacancy = PydanticVacancy(
                                resource_id=item.get('id'),
                                platform_id=platform.id,
                                name=item.get('name') if item.get('name') else '',
                                address=address.get('street') if address.get('street') else '',
                                salary_from=salary.get('from') if salary.get('from') else None,
                                salary_to=salary.get('to') if salary.get('to') else None,
                                gross=salary.get('gross') if salary.get('gross') else None,
                                url=item.get('url'),
                                requirement=snippet.get('requirement') if snippet.get('requirement') else '',
                                responsibility=snippet.get('responsibility') if snippet.get('responsibility') else '',
                                company='',
                                town_id=town.id,
                            )
                            objects.append(Vacancy(**vacancy.dict()))
                        except ValidationError as e:
                            _logger.error(f"Error occurred while collect vacancies from hh: {e}")
                else:
                    break
                page += 1
        except HTTPError as e:
            _logger.error(
                f"HTTP error occurred while collect vacancies from hh: {e}"
            )
            return
        except Exception as e:
            _logger.error(f"Error occurred while collect vacancies from hh: {e}")
            return

        session.query(Vacancy).filter(Vacancy.platform_id == platform.id).delete()
        session.bulk_save_objects(objects)
        session.commit()
