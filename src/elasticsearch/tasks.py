import logging

from src.celery_app.app import app
from src.elasticsearch.index import load_documents_to_index

_logger = logging.getLogger(__name__)


@app.task
def reindex_elasticsearch():
    load_documents_to_index()
