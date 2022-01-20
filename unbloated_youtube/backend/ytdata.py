from constants import Common, RePatterns
from defaultrequest import DefaultRequest
import re
import json


class Recommendation:
    """
    class to represent a recommendation video.
    """
    def __init__(self, title, url):
        self.title = title
        self.length = 0 
        self.url = url
        self.date = None
        self.views = 0
        self.thumbnail = None


class YtData(DefaultRequest):
    """
    this class respresents the var `ytIntialData` in every video html source code.
    it has information about count of subscribers, likes, recommandations, and more.

    """
    def __init__(self, url, headers, html=None, start=False, is_video=False):
        super().__init__(url, headers, html, start)
        self.is_video = is_video

    def getdata(self):
        """
        gets youtube data variable, and transforms it into a dictionary
 
        :return: dict
        """
        if self.is_video:
            # TODO: optimize regex
            self.result = re.search(RePatterns.DATA_PATTERN, self.result).group(0)
            self.result = self.result.replace(Common.VAR_YTDATA, "").strip()
            self.result = self.result.replace("=", "", 1).strip()
            self.result = self.result.replace(";</script", "")
            self.convert_json()
        return self.result
  
    def get_primary_info(self):
        return self.result['contents']['twoColumnWatchNextResults']['results']['results']['contents'][0]['videoPrimaryInfoRenderer']

    def get_secondary_info(self):
        return self.result['contents']['twoColumnWatchNextResults']['results']['results']['contents'][1]['videoSecondaryInfoRenderer']

    def get_publisher_pfp(self, size=0):
        """
        gets the video publisher profile picture
        :param size: to set different sizes, use the enum `Sizes` in constants.py
        :return: link to url
        """
        return self.get_secondary_info()['owner']['videoOwnerRenderer']['thumbnail']['thumbnails'][size]['url']  # smallest type

    def get_channel_name(self):
        return self.get_secondary_info()['owner']['videoOwnerRenderer']['title']['runs'][0]['text']

    def get_channel_url(self):
        return Common.YOUTUBE_URL + self.get_secondary_info()['owner']['videoOwnerRenderer']['title']\
                                                             ['runs'][0]['navigationEndpoint']\
                                                             ['browseEndpoint']['canonicalBaseUrl']

    def get_subscribers(self):
        return self.get_secondary_info()['owner']['videoOwnerRenderer']['subscriberCountText']['simpleText']

    def get_description(self):
        return self.get_secondary_info()['description']['runs'][0]['text']

    def get_views(self, short=True):
        """
        short view count, or full view count
        """
        if not short:
            return self.get_primary_info()['viewCount']['videoViewCountRenderer']['viewCount']['simpleText']
        return self.get_primary_info()['viewCount']['videoViewCountRenderer']['shortViewCount']['simpleText']

    def get_title(self):
        return self.get_primary_info()['title']['runs'][0]['text']

    def get_date(self):
        return self.get_primary_info()['dateText']['simpleText']

    def get_likes(self, short=True):
        if not short:
            return self.get_primary_info()['videoActions']['menuRenderer']['topLevelButtons'][0]\
                    ['toggleButtonRenderer']['defaultText']['accessibility']['accessibilityData']['label']
        return self.get_primary_info()['videoActions']['menuRenderer']['topLevelButtons'][0]\
                ['toggleButtonRenderer']['defaultText']['simpleText']
    
    def get_url(self):
        return self.url

    def get_secondary_results(self):
        return self.result['contents']['twoColumnWatchNextResults']['secondaryResults']['secondaryResults']['results']

    def get_recommendations(self):
        """
        fetches recommendations that are related to this video.
        WARNING: currently only returns smallest size of thumbnails.
        :return: yields current recommendation: (thumbnail, )
        """
        secondary_results = self.get_secondary_results()
        for recommend in secondary_results:
            if 'compactVideoRenderer' not in recommend.keys():
                break 
            recommend = recommend['compactVideoRenderer']
            title = recommend['title']['simpleText']
            url = Common.YOUTUBE_URL + recommend['navigationEndpoint']['commandMetadata']\
                                                ['webCommandMetadata']['url']
            obj = Recommendation(title, url)
            obj.thumbnail = recommend['thumbnail']['thumbnails'][0]['url']
            if 'lengthText' in recommend.keys():  # it could be a live video (same for the two other conditions)
                obj.length = recommend['lengthText']['simpleText']
            if 'publishedTimeText' in recommend.keys():
                obj.date = recommend['publishedTimeText']['simpleText']
            if 'simpleText' in recommend['viewCountText'].keys():
                obj.views = recommend['viewCountText']['simpleText']
            yield obj

    def get_continuation_token_comments(self):
        """
        returns the start continuation token for comments
        WARNING: only the first one.
        """
        return self.result['contents']['twoColumnWatchNextResults']['results']['results']['contents'][2]\
                        ['itemSectionRenderer']['contents'][0]['continuationItemRenderer']\
                        ['continuationEndpoint']['continuationCommand']['token']


    def get_continuation_token_videos(self):
        """
        returns the start continuation token for recommended videos.
        the continuation token is on the last recommended video, which it makes-
        sense.
        WARNING: only the first token.
        """
        secondary_results = self.get_secondary_results()
        last_recommended = secondary_results[-1]
        return last_recommended['continuationItemRenderer']['continuationEndpoint']['continuationCommand']['token']

