import backend.features
from backend.constants import Urls
from . import HEADERS, YTCFG_OBJ


def search_suggestions(query):
    search_link = YTCFG_OBJ.get_search_suggestions_url()
    return backend.features.autocomplete_search(search_link=search_link, query=query, headers=HEADERS)
