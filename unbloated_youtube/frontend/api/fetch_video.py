from . import YTCFG_OBJ, YTDATA_OBJ, RECOMMENDATIONS_OBJ


def fetch_video(video_url, quality, hdr=False):
    """
    Returning video googlevideo URL.

    :param video_url: YouTube URL
    """
    YTCFG_OBJ.is_video = True
    YTCFG_OBJ.set_url(video_url)
    YTCFG_OBJ.make_request()
    YTCFG_OBJ.getconfig()
    YTCFG_OBJ.is_video = False
    qualities = YTCFG_OBJ.get_qualities(hdr=hdr)
    if quality not in qualities:  # if the video doesn't have this quality (works also for "best" quality)
        quality = qualities[0]
    urls = YTCFG_OBJ.get_urls_by_quality(quality)

    return urls, qualities


def get_video_src():
    return YTCFG_OBJ.get_result() or YTDATA_OBJ.get_result()


def get_video_info(url=None, html=None):
    """
    Function to get basic video information such at the title and description.

    :param url: Video url. Don't have to specify if we haven't requested a new video,
    so we can save requests.
    """
    if url is not None:
        YTDATA_OBJ.is_video = True
        if html is None:
            YTDATA_OBJ.set_url(url)
            YTDATA_OBJ.make_request()
            YTDATA_OBJ.getdata()
        else:
            YTDATA_OBJ.getdata(html)
        YTDATA_OBJ.is_video = False 
    info = YTDATA_OBJ.get_video_info()
    return info


def get_recommendations(more=False):
    """
    Function to receive recommendations from YouTube.
    :param more: True if receive more commendations
    :return: list of Recommendation object
    """
    recommendations = list(YTDATA_OBJ.get_recommendations())
    if more:
        con_token = YTDATA_OBJ.get_continuation_token_videos()
        RECOMMENDATIONS_OBJ.set_con_token(con_token) 
        RECOMMENDATIONS_OBJ.recommend()
        recommendations = recommendations + list(RECOMMENDATIONS_OBJ.get_recommendations())
    return recommendations

