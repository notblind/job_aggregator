from datetime import datetime, timedelta

from src.vacancies.constants import PLATFORM_CODE
from src.vacancies.external_api.api import ExternalApi
from src.vacancies.models import Vacancy
from src.vacancies.pydantic_models import PydanticVacancy


class CollectVacancies(ExternalApi):
    NAME_DATA = ""

    def _collect_vacancies(self, platform, town, params):
        for data in self.get_paginated_data("GET", platform.url, params):
            vacancies = data.get(self.NAME_DATA)
            if vacancies:
                yield [
                    Vacancy(**self.prepare_data(platform, town, vacancy))
                    for vacancy in vacancies
                ]

    def prepare_data(self, platform, town, data):
        raise NotImplementedError("Please Implement this method")


class PlatformHH(CollectVacancies):
    NAME_DATA = "items"
    LIMIT = 100
    PAGE = 1

    def collect_vacancies(self, platform, town):
        if not platform or platform.name != PLATFORM_CODE.HH:
            return []
        params = {
            "per_page": self.LIMIT,
            "page": self.PAGE,
            "date_from": (datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m-%d"),
            "area": town.resource_id,
        }
        return self._collect_vacancies(platform, town, params)

    def prepare_data(self, platform, town, data):
        address = data.get("address", {})
        salary = data.get("salary", {})
        snippet = data.get("snippet", {})
        return PydanticVacancy(
            resource_id=data.get("id"),
            platform_id=platform.id,
            name=data.get("name", ""),
            address=address.get("street", ""),
            salary_from=salary.get("from"),
            salary_to=salary.get("to"),
            gross=salary.get("gross"),
            url=data.get("url", ""),
            requirement=snippet.get("requirement", ""),
            responsibility=snippet.get("responsibility", ""),
            company="",
            town_id=town.id,
        )

    def get_next_page(self, page, response):
        if response.get("pages") == response.get("page"):
            return None
        return page + 1


class PlatformVK(CollectVacancies):
    LIMIT = 50
    OFFSET = 0
    DEFAULT_PAGE_NAME = "offset"

    def collect_vacancies(self, platform, town):
        if not platform or platform.name != PLATFORM_CODE.VK:
            return []
        params = {"limit": self.LIMIT, "offset": self.OFFSET, "town": town.resource_id}
        return self._collect_vacancies(platform, town, params)

    def prepare_data(self, platform, town, data):
        return PydanticVacancy(
            resource_id=data.get("id"),
            platform_id=platform.id,
            name=data.get("title", ""),
            town_id=town.id,
        )

    def get_next_page(self, page, response):
        if not response.get("next"):
            return None
        return page + self.LIMIT
