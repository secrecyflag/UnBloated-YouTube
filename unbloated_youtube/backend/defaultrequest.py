import urllib.request
import urllib.parse
from exceptions import NoHeaders, NoPostData
import json


class DefaultRequest:
    """
    class to represent html/js tags/variables.

    """
    def __init__(self, url, headers=None, html=None, start=False, post_data=None):
        self.url = url
        self.req = None
        self.headers = headers
        self.result = html
        self.post_data = post_data
        if self.post_data is not None:
            self.post_data = post_data.encode()
        if start:
            self.make_request()

    def make_request(self, post=False, url=None):
        if self.headers is None:
            raise NoHeaders()
        if post:
            if self.post_data is None:
                raise NoPostData()
            self.req = urllib.request.Request(self.url, data=self.post_data)
        else:
            self.req = urllib.request.Request(self.url) 
        user_agent = self.headers["user-agent"] if "user-agent" in self.headers.keys() else self.headers["User-Agent"]
        self.req.add_header("User-Agent", user_agent)
        if "content-type" in self.headers.keys() or "Content-Type" in self.headers.keys():
            key = "Content-Type" if "Content-Type" in self.headers.keys() else "content-type"
            self.req.add_header("Content-Type", self.headers[key])
        if url is None:
            self.req = urllib.request.urlopen(self.req)
            self.result = self.req.read().decode("utf-8")
        else:
            req = urllib.request.Request(url) 
            req.add_header("User-Agent", user_agent)
            req = urllib.request.urlopen(req)
            result = req.read().decode("utf-8")
            return result

    @staticmethod
    def unquote_url(url):
        return urllib.parse.unquote(url)

    def get_request(self):
        return self.req

    def get_result(self):
        return self.result
    
    def get_url(self):
        return self.url

    def get_headers(self):
        return self.headers

    def convert_json(self):
        """
        converting `self.result` to json
        """
        self.result = json.loads(self.result)

