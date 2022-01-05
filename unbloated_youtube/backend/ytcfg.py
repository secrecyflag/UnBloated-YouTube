import re
from .constants import Common, RePatterns, Urls
from .defaultrequest import DefaultRequest
import json
import exceptions
import signature_decipher
import itags
# TODO: BETTER DOCS


class YtConfig(DefaultRequest):
    """
    Youtube config class.
    youtube html videos has a var called: "ytInitialPlayerResponse" it has some very useful information about the video, 
    such as url links, and quality video and so on.

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
        self.__base_js = None
        self.optimized = True 

    def getconfig(self):
        """
        gets youtube config variable
        :return: dict 
        """
        if self.req is None:
            return False
        if self.is_video:
            self.config = re.search(RePatterns.CONFIG_PATTERN, self.result)
            if self.config is None:
                return False
            self.config = self.config.group(0)
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
        if type_ == Common.MINUTES:
            seconds = duration // 1000
            minutes = 0
            while seconds >= 60:
                minutes += 1
                seconds -= 60
            return minutes, seconds
        else:
            return int(duration // 1000)
        return duration
    
    def get_quality(self, index):
        self.basic_exception_check()
        return self.get_adaptiveformats()[index]["qualityLabel"]

    def get_urls_by_quality(self, quality):
        self.basic_exception_check()
        urls = {"video": [], "audio": []}
        for format_ in self.get_adaptiveformats():
            if "signatureCipher" in format_.keys():
                signature_cipher = format_["signatureCipher"]
                signature_cipher = self.unquote_url(signature_cipher)
                url = self.decrypt_signature_and_pass_url(signature_cipher)
            else:
                url = format_["url"]
            if "qualityLabel" in format_.keys():  # if its mp4
                if format_["qualityLabel"] == quality:
                    urls["video"].append(url)
            else:
                urls["audio"].append(url)  # else its audio
        if self.optimized:
            urls["video"] = self.optimize(urls["video"])
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
            quality = format_["qualityLabel"]
            if quality in qualities:
                continue
            qualities.append(quality)
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

    def set_url(self, url):
        self.url = url

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

    def extract_encrypted_signature(self, text: str):
        signature_cipher = self.unquote_url(text)
        signature = re.search(RePatterns.SIGNATURE, signature_cipher).group()
        return signature

    def extract_url(self, text: str):
        url = re.search(RePatterns.URL, text).group(0)
        url = self.unquote_url(url) 
        return url

    def get_base_js(self):
        url = Urls.YOUTUBE_URL + self.config["WEB_PLAYER_CONTEXT_CONFIGS"]["WEB_PLAYER_CONTEXT_CONFIG_ID_KEVLAR_WATCH"]["jsUrl"]
        result = self.make_request(url=url)
        return result

    def decrypt_signature_and_pass_url(self, signature: str):
        url = self.extract_url(signature)
        signature = self.extract_encrypted_signature(signature)
        if self.__base_js is None:
            self.__base_js = self.get_base_js()
        decrypted = signature_decipher.decrypt(signature=signature, js=self.__base_js)
        url += "&sig=" + decrypted
        return url

    def optimize(self, urls: list):
        """
        EXPERIMENTAL!

        This method will choose the urls that are the most usable 
        for streaming, without getting any lags or buffer issues, 
        like video gets stuck every 0.1 seconds.

        The most best video codecs from left to right: AV1, VP9, H264.
        The first two are the most promising one in terms of efficiency.
        H264 codec seems to be more laggy and sometimes even not usable than the others.

        :param urls: googlevideo urls
        :return: False if self.optimize variable is False
        """
        if not self.optimize:
            return False 
        preferred_urls = {"AV1": [], "VP9": [], "H264": []}
        for url in urls:
            itag = re.search(RePatterns.ITAG_URL, url)
            if itag is None:
                continue
            itag = int(itag.group(0))
            if itag in itags.H264:
                preferred_urls["H264"].append(url)
            elif itag in itags.H264_HFR:
                preferred_urls["H264"].insert(0, url)
            elif itag in itags.VP9:
                preferred_urls["VP9"].append(url)
            elif itag in itags.VP9_HFR:
                preferred_urls["VP9"].insert(1, url)
            elif itag in itags.VP9_HDR_HFR:
                preferred_urls["VP9"].insert(0, url)
            elif itag in itags.AV1:
                preferred_urls["AV1"].append(url)
            elif itag in itags.AV1_HFR:
                preferred_urls["AV1"].insert(1, url)
            elif itag in itags.AV1_HDR_HFR:
                preferred_urls["AV1"].insert(0, url)
        return preferred_urls["AV1"] + preferred_urls["VP9"] + preferred_urls["H264"]

