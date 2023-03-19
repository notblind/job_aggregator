from celery.schedules import crontab

task_serializer = 'json'
result_serializer = 'json'
timezone = 'Europe/Moscow'
enable_utc = True
task_track_started = True

imports = ['src.vacancies.tasks', 'src.elasticsearch.tasks']

beat_schedule = {
    'collect_vacancies_from_hh': {
        'task': 'src.vacancies.tasks.collect_vacancies_from_hh',
        'schedule': crontab(hour=1)
    },
    'reindex_elasticsearch': {
        'task': 'src.elasticsearch.tasks.reindex_elasticsearch',
        'schedule': crontab(hour=6)
    }
}
