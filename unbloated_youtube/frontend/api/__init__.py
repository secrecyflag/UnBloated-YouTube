from unbloated_youtube.backend import ytcfg
from unbloated_youtube.backend.constants import Urls
from unbloated_youtube.backend import headers

HEADERS = {"User-Agent": headers.generate()}
YTCFG_OBJ = ytcfg.YtConfig(Urls.YOUTUBE_URL, headers=HEADERS, start=True, more=True, is_video=False)
YTCFG_OBJ.getconfig()

