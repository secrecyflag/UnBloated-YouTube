from . import HEADERS, YTCFG_OBJ


def fetch_video(video_url, quality="480p"):
    """
    Returning video googlevideo URL.

    :param video_url: YouTube URL
    :param quality: quality. Use Enum `Qualities`
    """
    YTCFG_OBJ.is_video = True
    YTCFG_OBJ.set_url(video_url)
    YTCFG_OBJ.make_request()
    YTCFG_OBJ.getconfig()
    YTCFG_OBJ.is_video = False
    urls = YTCFG_OBJ.get_urls_by_quality(quality)
    qualities = YTCFG_OBJ.get_qualities()
    return urls, qualities

