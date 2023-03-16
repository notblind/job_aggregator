import argparse
import logging
import sys

from elasticsearch import Elasticsearch

from src.settings import ELASTIC_URL, ELASTIC_INDEX
from src.elasticsearch.config import POSTS_INDEX_SETTINGS, POSTS_INDEX_MAPPINGS
from src.vacancies.document import get_hh_document


_logger = logging.getLogger(__name__)

es_client = Elasticsearch(ELASTIC_URL)


def recreate_index():
    """Rebuild the ES index."""
    es_client.options(ignore_status=404).indices.delete(index=ELASTIC_INDEX)
    logging.info("Index `%s` is deleted if existing.", ELASTIC_INDEX)
    es_client.indices.create(
        index=ELASTIC_INDEX,
        settings=POSTS_INDEX_SETTINGS,
        mappings=POSTS_INDEX_MAPPINGS,
    )
    _logger.info("Index `%s` is (re-)created.", ELASTIC_INDEX)


def load_documents_to_index():
    """Load post documents to the Elasticsearch index."""
    es_actions = []

    data = get_hh_document()

    for item in data:
        action = {
            "index": {"_index": ELASTIC_INDEX, "_id": item.pop("id")}
        }
        es_actions.append(action)
        es_actions.append(item)

    es_client.bulk(
        index=ELASTIC_INDEX,
        operations=es_actions,
        filter_path="took,errors",
    )

    _logger.info("%s items have been indexed.", len(data))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-r',
        '--recreate',
        dest='recreate_index',
        action='store_true',
        help='''
            If True, the old index will be deleted if existing before a
            new one is created.
            ''',
    )

    args = parser.parse_args()

    if (
        not es_client.indices.exists(index=ELASTIC_INDEX)
        or args.recreate_index
    ):
        recreate_index()

    try:
        load_documents_to_index()
    except Exception as exc:
        logging.exception(exc)
        sys.exit(1)
    finally:
        es_client.close()
