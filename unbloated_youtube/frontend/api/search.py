import backend.features
from backend.constants import Urls
from . import HEADERS, YTCFG_OBJ, INNERTUBE_API, INNERTUBE_CONTEXT


# def search_suggestions(query):  # TODO: return to this later
#     search_link = YTCFG_OBJ.get_search_suggestions_url()
#     return backend.features.autocomplete_search(search_link=search_link, query=query, headers=HEADERS)


SEARCH = backend.features.Search(query="", 
                                 innertube_api=INNERTUBE_API, 
                                 innertube_context=INNERTUBE_CONTEXT,
                                 headers=HEADERS)


def search_results(query):
    SEARCH.set_query(query)
    SEARCH.search()
    for result in SEARCH.get_next_search_result():
        yield result

