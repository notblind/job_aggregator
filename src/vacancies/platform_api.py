import logging
import time
from datetime import datetime, timedelta

import requests
from fastapi import status
from pydantic import ValidationError

from src.vacancies.constants import PLATFORM_CODES
from src.vacancies.models import Vacancy
from src.vacancies.pydantic_models import PydanticVacancy

_logger = logging.getLogger(__name__)


def collect_vacancies_from_hh(platform, towns):
    params = {
        'per_page': 100,
        'page': 0,
        'date_from': (datetime.utcnow() - timedelta(days=30)).strftime('%Y-%m-%d')
    }
    objects = []
    if not platform or platform.name != PLATFORM_CODES.HH:
        return objects

    for town in towns:
        params['area'] = town.resource_id
        page = 0
        next_page = True
        _logger.error(town.name)
        while page < 40 and next_page:
            params['page'] = page
            response = requests.get(platform.url, params=params)
            if response.status_code == status.HTTP_200_OK:
                res_json = response.json()
                items = res_json.get('items')
                next_page = bool(res_json.get('pages') != res_json.get('page'))
                for item in items:
                    try:
                        address = item.get('address') if item.get('address') else {}
                        salary = item.get('salary') if item.get('salary') else {}
                        snippet = item.get('snippet') if item.get('snippet') else {}
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
                        _logger.error(f'Error occurred while collect vacancies from hh: {e}')
            else:
                _logger.error(f'Response status is not 200')
                next_page = False
            page += 1
            time.sleep(0.1)
    return objects


def collect_vacancies_from_vk(platform, towns):
    params = {
        'limit': 50,
        'offset': 0,
    }
    objects = []
    if not platform or platform.name != PLATFORM_CODES.VK:
        return objects

    for town in towns:
        params['town'] = town.resource_id
        offset = 0
        next_page = True
        while offset < 1000 and next_page:
            params['offset'] = offset
            response = requests.get(platform.url, params=params)
            if response.status_code == status.HTTP_200_OK:
                res_json = response.json()
                items = res_json.get('results')
                next_page = bool(res_json.get('next'))
                for item in items:
                    try:
                        vacancy = PydanticVacancy(
                            resource_id=item.get('id'),
                            platform_id=platform.id,
                            name=item.get('title') if item.get('title') else '',
                            town_id=town.id,
                        )
                        objects.append(Vacancy(**vacancy.dict()))
                    except ValidationError as e:
                        _logger.error(f'Error occurred while collect vacancies from vk: {e}')
            else:
                _logger.error(f'Response status is not 200')
                next_page = False
            offset += 50
            time.sleep(0.1)
    return objects
