POSTS_INDEX_SYNONYMS = [
    "es, elasticsearch",
    "js, javascript",
    "ts, typescript",
    "k8s, k9s, Kubernetes",
]

POSTS_INDEX_SETTINGS = {
    "analysis": {
        "analyzer": {
            "post_index_analyzer": {
                "type": "custom",
                "tokenizer": "standard",
                "filter": [
                    "lowercase",
                    "autocomplete_filter",
                ],
            },
            "post_search_analyzer": {
                "type": "custom",
                "tokenizer": "standard",
                "filter": [
                    "lowercase",
                    "synonym_filter",
                ],
            },
        },
        "filter": {
            "synonym_filter": {
                "type": "synonym_graph",
                "expand": True,
                "lenient": True,
                "synonyms": POSTS_INDEX_SYNONYMS,
            },
            "autocomplete_filter": {
                "type": "edge_ngram",
                "min_gram": 1,
                "max_gram": 20,
            },
        },
    },
}

POSTS_INDEX_MAPPINGS = {
    "properties": {
        "address": {"type": "text"},
        "town": {"type": "text"},
        "salary_from": {"type": "float"},
        "salary_to": {"type": "float"},
        "title": {
            "type": "text",
            "search_analyzer": "post_search_analyzer",
            "fields": {
                "ngrams": {
                    "type": "text",
                    "analyzer": "post_index_analyzer",
                    "search_analyzer": "post_search_analyzer",
                },
            },
        },
    }
}
