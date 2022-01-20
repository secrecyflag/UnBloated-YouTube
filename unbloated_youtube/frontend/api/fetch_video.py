from . import YTCFG_OBJ, YTDATA_OBJ


def fetch_video(video_url, quality):
    """
    Returning video googlevideo URL.

    :param video_url: YouTube URL
    """
    YTCFG_OBJ.is_video = True
    YTCFG_OBJ.set_url(video_url)
    YTCFG_OBJ.make_request()
    YTCFG_OBJ.getconfig()
    YTCFG_OBJ.is_video = False
    qualities = YTCFG_OBJ.get_qualities()
    if quality not in qualities:  # if the video doesn't have this quality (works also for "best" quality)
        quality = qualities[-1]
    urls = YTCFG_OBJ.get_urls_by_quality(quality)
        
    return urls, qualities


def get_video_title(url=None):
    """

    :param url: Video url. Don't have to specify if we haven't requested a new video,
    so we can save requests.
    :return: video title
    """
    if url is not None:
        YTDATA_OBJ.is_video = True
        YTDATA_OBJ.set_url(url)
        YTDATA_OBJ.make_request()
        YTDATA_OBJ.getdata()
        YTDATA_OBJ.is_video = False 
    return YTDATA_OBJ.get_title()
