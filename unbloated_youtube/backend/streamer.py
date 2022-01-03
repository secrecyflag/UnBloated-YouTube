import urllib.request 
import exceptions
import re
from constants import RePatterns, Common
import subprocess
import threading


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
        self._start_range = 0
        self.__video_file = None
        self.__current_position = 0

    @property
    def start_range(self):
        return self._start_range
    
    @start_range.setter
    def range(self, range_):
        self._start_range = range_

    @property
    def current_position(self):
        pass

    @current_position.setter
    def current_position(self, position):
        self.__current_position = position

    @staticmethod
    def get_best_url(urls: list) -> str:
        """
        
        :param urls: dict: {video: [urls],
                            audio: [urls]}
        :return: (video url, audio urls)
        """
        video_url = urls["video"][0]  # Temporary
        audio_url = urls["audio"][0]  # Temporary
        return video_url, audio_url 
        
    def stream(self, duration, quality, path=None):
        """
        loads approx 7MB of bytes, and yields it
    
        :param path: if specified a path, this method will create a new file, and
        append to it the fetched data. most include a name and a file format (e.g. x.mp4)
        :yield: bytes object
        """
        self.duration = duration
        url = self.get_best_url(self.config.get_urls_by_quality(quality))
        len_bytes = int(re.search(RePatterns.CLEN_PATTERN, url[0]).group(0).replace("clen=", ""))  # filesize/contentLength in bytes
        if path is None:
            return True
            end_range = 0
            while end_range < len_bytes:
                    end_range = min(len_bytes, self._start_range + Common.RANDOM_RANGE)
                    stream_url = url + "&range={0}-{1}".format(self._start_range, end_range)  # adding range payload
                    req = urllib.request.Request(stream_url)
                    req.add_header("user-agent", self.headers["user-agent"])
                    response = urllib.request.urlopen(req)
                    chunk = response.read()
                    # yield chunk
                    self._start_range += len(chunk)
        else:
            args = ["ffmpeg", "-y",
                    "-ss", str(self.__current_position),
                    "-headers", "user-agent: " + self.headers["User-Agent"],
                    "-i", url[0],
                    "-t", str(self.duration),
                    "-c:v", "copy", "-c:a", "copy",
                    path]

            thread = threading.Thread(target=subprocess.Popen, kwargs={"args": args, "stdout": subprocess.PIPE, "stderr": subprocess.PIPE})
            thread.start()

