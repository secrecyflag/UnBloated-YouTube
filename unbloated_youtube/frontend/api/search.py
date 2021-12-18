import backend.features
from backend.constants import Urls


def search_suggestions(query):
    return backend.features.autocomplete_search(search_link=Urls.YOUTUBE_SEARCH, query=query, headers=headers)
