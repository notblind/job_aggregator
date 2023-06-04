from datetime import datetime, timedelta

from src.vacancies.external_api.api import ExternalApi
from src.vacancies.models import Vacancy
from src.vacancies.pydantic_models import PydanticVacancy


class CollectVacancies(ExternalApi):
    KEY_DATA = ""
    KEY_TOWN = ""

    def _collect_vacancies(self, platform, towns, params):
        for town in towns:
            params[self.KEY_TOWN] = town.resource_id
            for data in self.get_paginated_data("GET", platform.url, params):
                vacancies = data.get(self.KEY_DATA)
                if vacancies:
                    yield [
                        Vacancy(**self.prepare_data(platform, town, vacancy))
                        for vacancy in vacancies
                    ]

    def prepare_data(self, platform, town, data):
        raise NotImplementedError("Please Implement this method")


class PlatformHH(CollectVacancies):
    KEY_DATA = "items"
    KEY_TOWN = "area"
    LIMIT = 100
    LIMIT_DATA = 20

    def collect_vacancies(self, platform, towns):
        params = {
            "per_page": self.LIMIT,
            "date_from": (datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m-%d"),
        }
        return self._collect_vacancies(platform, towns, params)

    def prepare_data(self, platform, town, data):
        data = {key: value for key, value in data.items() if value is not None}
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
        ).dict()

    def get_next_page(self, page, response):
        if response.get("pages") == response.get("page"):
            return None
        return page + 1


class PlatformVK(CollectVacancies):
    LIMIT = 50
    DEFAULT_PAGE_NAME = "offset"
    KEY_DATA = "results"
    KEY_TOWN = "town"

    def collect_vacancies(self, platform, towns):
        params = {"limit": self.LIMIT}
        return self._collect_vacancies(platform, towns, params)

    def prepare_data(self, platform, town, data):
        return PydanticVacancy(
            resource_id=data.get("id"),
            platform_id=platform.id,
            name=data.get("title", ""),
            town_id=town.id,
        ).dict()

    def get_next_page(self, page, response):
        if not response.get("next"):
            return None
        return page + self.LIMIT
