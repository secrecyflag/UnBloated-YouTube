from unbloated_youtube.backend import ytcfg
from unbloated_youtube.backend.constants import Urls

HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/532.0 (KHTML'}  # TODO: implement headers.py
YTCFG_OBJ = ytcfg.YtConfig(Urls.YOUTUBE_URL, headers=HEADERS, start=True, more=True)


