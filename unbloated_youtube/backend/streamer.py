import urllib.request 
import exceptions
import re
from constants import RePatterns, Common


class Stream:
    """
    Stream class.
    helps with streaming any kind of youtube videos.
    passing age restriction isn't part of it.
    """
    def __init__(self, config: "YtConfig", quality, headers, auto: bool=False):
        """
        constructor

        :param config: youtube config object
        :param quality: chosen quality
        :param auto: True if to change the quality based on internet speed
        """
        self.curr_position = 0  # current position in video/audio
        self.config = config
        self.quality = quality
        self.duration = self.config.get_duration()
        self.auto = auto  # TODO: add algorithm to determine the best url/quality based on the internet speed
        self.headers = headers

    @staticmethod
    def get_best_url(data: list, quality) -> str:
        """
        sometimes there could be the same quality with multiple googlevideo urls, 
        this function will choose the url according to codec. AV1 is the best in terms of quality, but takes a little bit more resources 
        and VP9 is the standard on google platforms.
        
        :param data: dict: {video/audio: {codec: {quality: url}/url}}
        :return: final URL
        """
        if len(data) == 1:
            return urls[0]
        url = None
        for codec in data['video'].keys():
            codec_dict = data['video'][codec]
            if quality not in codec_dict.keys():
                continue
            if "vp9" in codec:  # VP9 is preferred
                return codec_dict[quality]
            else:  # if for some reason there is no VP9 encoding
                url = codec_dict[quality]
        if url is None:  # if there is no such quality
            raise exceptions.NoSuchVideoQuality()
        return url
        
    def __iter__(self):
        for buffer in self.stream():
            yield buffer

    def stream(self, parallel=False):
        """
        loads approx 7MB of bytes, and yields it
    
        :yield: bytes object
        """
        url = self.get_best_url(self.config.get_basic(), self.quality)  # getting the best URL for streaming
        len_bytes = int(re.search(RePatterns.CLEN_PATTERN, url).group(0).replace("clen=", ""))  # filesize/contentLength in bytes
        start_range = 0
        end_range = 0
        while end_range < len_bytes:
            end_range = min(len_bytes, start_range + Common.RANDOM_RANGE)
            stream_url = url + "&range={0}-{1}".format(start_range, end_range)  # adding range payload
            req = urllib.request.Request(stream_url)
            req.add_header("user-agent", self.headers['user-agent'])
            response = urllib.request.urlopen(req)
            chunk = response.read()
            yield chunk
            start_range += len(chunk)
        
