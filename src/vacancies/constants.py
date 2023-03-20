from enum import Enum

APP_VACANCIES = 'vacancies'
SEARCH_FIELDS = ['id', 'address', 'town_id', 'salary_from', 'salary_to', 'name']


class PLATFORM_CODES(str, Enum):
    VK = 'vk'
    HH = 'hh'
