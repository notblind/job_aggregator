from enum import Enum

APP_VACANCIES = 'vacancies'
SEARCH_FIELDS = ['id', 'address', 'town_id', 'salary_from', 'salary_to', 'name']

# Httpx
HTTPX_TIMEOUT = 2
HTTPX_KEEP_ALIVE = 5
HTTPX_MAX_CONNECTIONS = 10


class PLATFORM_CODES(str, Enum):
    VK = 'vk'
    HH = 'hh'
