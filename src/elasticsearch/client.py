from elasticsearch import Elasticsearch

from src.settings import ELASTIC_URL


def get_es_client():
    es_client = Elasticsearch(ELASTIC_URL)

    try:
        yield es_client
    finally:
        es_client.close()
