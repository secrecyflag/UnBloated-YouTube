import re
from .constants import Common, RePatterns
from .defaultrequest import DefaultRequest
import json
import exceptions


class YtConfig(DefaultRequest):
    """
    Youtube config class.
    youtube html videos has a var called: "ytInitialPlayerResponse" it has some very useful information about the video, such as url links, and quality video and so on.

    """
    def __init__(self, url, headers, html=None, start=False, more=False, is_video=True):
        """
        
        :param start: make request right away when creating object
        :param more: there is additional information from youtube config, 
        which can be found in `ytcfg.set...` calls.
        :param is_not_video: specifying if we're not in any YouTube video. useful if there is no ytInitialPlayerResponse variable
        """
        super().__init__(url, headers, html, start)
        self.config = {}
        self.more = more
        self.is_video = is_video

    def getconfig(self):
        """
        gets youtube config variable
        :return: dict 
        """
        if self.req is None:
            return False
        if self.is_video:
            self.config = re.search(RePatterns.CONFIG_PATTERN, self.result).group(0)
            self.config = self.config.replace(Common.VAR_YTCONFIG, "").strip()
            self.config = self.config.replace("=", "", 1).strip()
            self.config = self.config.replace(";</", "")
            self.config = json.loads(self.config)
        if self.more:  # if requested for additional information
            additional = re.search(RePatterns.YTCFG_MORE, self.result).group(0)
            additional = additional.replace(");", "").strip()
            additional = additional.replace("ytcfg.set(", "")
            additional = json.loads(additional)
            self.config.update(additional)
        return self.config
    
    def get_adaptiveformats(self):
        self.basic_exception_check()
        return self.config[Common.STREAMINGDATA][Common.ADAPTIVEFORMATS]

    def get_url_quality(self):
        """
        returns url links and qualities generator

        """
        self.basic_exception_check()
        formats = self.get_adaptiveformats()
        for format_ in formats:
            yield unquote(format_["url"]), format_["qualityLabel"]
    
    def get_url(self):
        self.basic_exception_check()
        formats = self.get_adaptiveformats()
        for format_ in formats:
            yield unquote(format_["url"])

    def get_duration(self, type_=None):
        self.basic_exception_check()
        duration = int(self.get_adaptiveformats()[0][Common.DURATION])
        if type_ == Common.SECONDS:
            return duration // 1000
        elif type_ == Common.MINUTES:
            seconds = duration // 1000
            minutes = 0
            while seconds >= 60:
                minutes += 1
                seconds -= 60
            return minutes, seconds
        return duration
    
    def get_quality(self, index):
        self.basic_exception_check()
        return self.get_adaptiveformats()[index]["qualityLabel"]


    def is_age_restricted(self) -> bool:
        return "signatureCipher" in self.get_adaptiveformats()[0].keys()

    def get_urls_by_quality(self, quality):
        self.basic_exception_check()
        urls = {"video": [], "audio": []}
        for format_ in self.get_adaptiveformats():
            if "qualityLabel" in format_.keys():  # if its mp4
                if format_["qualityLabel"] == quality:
                    urls["video"].append(format_["url"]) 
            else:
                urls["audio"].append(format_["url"])  # else its audio
        return urls if len(urls) > 0 else False 
    
    def get_qualities(self):
        """
        returns the available qualities for watching this video

        :return: available qualities, list
        """
        self.basic_exception_check()
        qualities = []
        for format_ in self.get_adaptiveformats():
            if "audio" in format_["mimeType"]:
                continue
            qualities.append(format_["qualityLabel"])
        return qualities

    def get_basic(self):
        """
        method to get the basic information on the video, such as urls with quality, type, codec
        
        :return: dict
        """
        self.basic_exception_check()
        info = {"video": {}, "audio": {}}

        for format_ in self.get_adaptiveformats():
            codec = format_["mimeType"].split(";")  # format of mimeType is = (video/audio)/(mp4/web); codecs=...
            type_ = codec[0]
            codec = codec[1].replace("codecs=\"", "")[1:-1]
            if codec not in info.keys():
                if type_.startswith("audio"):
                    info["audio"][codec] = format_["url"]
                else:
                    quality = format_["qualityLabel"]
                    info["video"][codec] = {quality: format_["url"]}
            else:
                info[codec][quality] = format_["url"]
        return info

    def get_innertube_api(self):
        self.basic_exception_check(True) 
        return self.config["INNERTUBE_API_KEY"]

    def get_innertube_context(self):
        self.basic_exception_check(True)
        return {"context": self.config["INNERTUBE_CONTEXT"]}

    def get_link_api(self):
        self.basic_exception_check(True)
        return self.config["LINK_API_KEY"]

    def get_search_suggestions_url(self):
        self.basic_exception_check(True)
        return "https://" + self.config["SBOX_SETTINGS"]["SEARCHBOX_HOST_OVERRIDE"] + "/complete/search?client=youtube&q={0}"

    def basic_exception_check(self, more=False):
        """
        method to check if the majority of the other methods will work
        
        :return: 
        """

        if self.config is None:
            raise exceptions.RaiseIsEmpty()
        if more:
            if not self.more:
                raise exceptions.NoAdditionalInformation()

