from celery.schedules import crontab

from src.vacancies.constants import PLATFORM_CODE

task_serializer = "json"
result_serializer = "json"
timezone = "Europe/Moscow"
enable_utc = True
task_track_started = True

imports = ["src.vacancies.tasks", "src.elasticsearch.tasks"]

beat_schedule = {
    "collect_vacancies_from_hh": {
        "task": "src.vacancies.tasks.collect_vacancies",
        "schedule": crontab(hour=1),
        "args": (PLATFORM_CODE.HH.value,),
    },
    "collect_vacancies_from_vk": {
        "task": "src.vacancies.tasks.collect_vacancies",
        "schedule": crontab(hour=2),
        "args": (PLATFORM_CODE.VK.value,),
    },
    "reindex_elasticsearch": {
        "task": "src.elasticsearch.tasks.reindex_elasticsearch",
        "schedule": crontab(hour=6),
    },
}
