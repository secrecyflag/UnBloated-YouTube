from unbloated_youtube.backend import ytcfg, ytdata
from unbloated_youtube.backend.constants import Urls
from unbloated_youtube.backend import headers
import unbloated_youtube.backend.features as yt_features

HEADERS = {"User-Agent": headers.generate()}
YTCFG_OBJ = ytcfg.YtConfig(Urls.YOUTUBE_URL, headers=HEADERS, start=True, more=True, is_video=False)
YTCFG_OBJ.getconfig()

YTDATA_OBJ = ytdata.YtData(Urls.YOUTUBE_URL, headers=HEADERS, start=True, is_video=False)
YTDATA_OBJ.getdata()

INNERTUBE_API = YTCFG_OBJ.get_innertube_api()
INNERTUBE_CONTEXT = YTCFG_OBJ.get_innertube_context()

RECOMMENDATIONS_OBJ = yt_features.Recommendations(INNERTUBE_API, INNERTUBE_CONTEXT, HEADERS, None)

