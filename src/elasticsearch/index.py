import argparse
import json
import logging
import pathlib
import sys

from elasticsearch import Elasticsearch

from src.elasticsearch.config import POSTS_INDEX_SETTINGS, POSTS_INDEX_MAPPINGS


_logger = logging.getLogger(__name__)

es_client = Elasticsearch('http://localhost:9200')

POSTS_INDEX_NAME = 'vacancy'
POSTS_DATA_PATH = pathlib.Path(__file__).parent.parent.joinpath(
    "data/Lynn-Kwong-Medium-Posts.json"
)


def recreate_index():
    """Rebuild the ES index."""
    es_client.options(ignore_status=404).indices.delete(index=POSTS_INDEX_NAME)
    logging.info("Index `%s` is deleted if existing.", POSTS_INDEX_NAME)
    es_client.indices.create(
        index=POSTS_INDEX_NAME,
        settings=POSTS_INDEX_SETTINGS,
        mappings=POSTS_INDEX_MAPPINGS,
    )
    _logger.info("Index `%s` is (re-)created.", POSTS_INDEX_NAME)


def load_documents_to_index():
    """Load post documents to the Elasticsearch index."""
    es_actions = []

    posts = [] # data from bd

    for post in posts:
        # Note that the _id field is not allowed in Elasticsearch as it's a builtin field.
        action = {
            "index": {"_index": POSTS_INDEX_NAME, "_id": post.pop("_id")}
        }
        es_actions.append(action)
        es_actions.append(post)

    es_client.bulk(
        index=POSTS_INDEX_NAME,
        operations=es_actions,
        filter_path="took,errors",
    )

    _logger.info("%s posts have been indexed.", len(posts))


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
        not es_client.indices.exists(index=POSTS_INDEX_NAME)
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
