#!/usr/bin/python3
from .defaultrequest import DefaultRequest
from .constants import Urls, RePatterns
import json
import urllib
import re
from . import exceptions


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


class Comments(DefaultRequest):
    """
    class to represent a comment
    """
    def __init__(self, innertube_api, innertube_context, continuation_token, headers=None):
        self.url = Urls.YOUTUBE_NEXT_URL.format(innertube_api)
        innertube_context.update({"continuation": continuation_token})
        self.innertube_context = innertube_context
        headers["Content-Type"] = "application/json"
        super().__init__(url=self.url, headers=headers)
        self.comments = None
        self.current_comment = None

    def get_comments(self, more=False):
        """
        getting the comments dictionary
        :param more: specifiying to get more comments. only if this method was already called atleast once
        """
        self.post_data = json.dumps(self.innertube_context).encode()
        self.make_request(post=True)
        self.convert_json()
        if more:
            self.comments = self.result["onResponseReceivedEndpoints"][0]["appendContinuationItemsAction"]["continuationItems"]
        else:
            self.comments = self.result["onResponseReceivedEndpoints"][1]["reloadContinuationItemsCommand"]["continuationItems"]

    def get_count_comments(self):
        return self.result["onResponseReceivedEndpoints"][0]["reloadContinuationItemsCommand"]["continuationItems"][0]\
                          ["commentsHeaderRenderer"]["countText"]["runs"][0]["text"]
    
    def get_next_comment(self, size=0):
        # ignoring last "comment", since it has the continuation token and different keys
        for comment in self.comments[:-1]:  
            comment_dict = {}
            self.current_comment = comment["commentThreadRenderer"]
            if "replies" in self.current_comment.keys():  # if comment has replies, it also has the continuation token for receiving more comments (replies)
                comment_dict["continuation"] = self.current_comment["replies"]["commentRepliesRenderer"]["contents"][0]\
                                                                   ["continuationItemRenderer"]["continuationEndpoint"]["continuationCommand"]["token"]
            self.current_comment = self.current_comment["comment"]["commentRenderer"]
            comment_dict["name"] = self.current_comment["authorText"]["simpleText"]
            comment_dict["pfp_url"] = self.current_comment["authorThumbnail"]["thumbnails"][size]["url"]
            comment_dict["content"] = self.current_comment["contentText"]["runs"][0]["text"]
            comment_dict["date"] = self.current_comment["publishedTimeText"]["runs"][0]["text"]
            comment_dict["is_liked_by_owner"] = True if "authorCommentBadge" in self.current_comment.keys() else False
            comment_dict["is_owner"] = self.current_comment["authorIsChannelOwner"]
            comment_dict["votes"] = self.current_comment["voteCount"]["simpleText"] if "votes" in self.current_comment.keys() else 0
            comment_dict["is_pinned"] = True if "pinnedCommentBadge" in self.current_comment.keys() else False
            comment_dict["reply_count"] = self.current_comment["replyCount"] if "replyCount" in self.current_comment.keys() else 0
            yield comment_dict

    def get_continuation_token(self):
        return self.comments[len(self.comments) - 1]["continuationItemRenderer"]["continuationEndpoint"]["continuationCommand"]["token"]

    def get_more_comments(self):
        self.innertube_context["continuation"] = self.get_continuation_token()
        self.get_comments(True)


def autocomplete_search(search_link, query, headers=None):
    """
    function to get search results
    this is not the greatest approach for autocomplete search, but for- 
    now its good.

    :param search_link: youtube search URL. most include a `q=` parameter
    """
    req = urllib.request.Request(search_link.format(query))
    user_agent = headers["User-Agent"] if "User-Agent" in headers.keys() else headers["user-agent"]
    if headers is not None:
        req.add_header("User-Agent", user_agent)
    print(search_link.format(query))
    results = urllib.request.urlopen(req).read().decode("utf-8")
    results = re.search(RePatterns.SEARCH_RESULTS, results).group()
    # reformatting
    results = re.sub(RePatterns.SEARCH_RESULTS_SUB, "", results)
    results = re.sub("{.*", "", results)  # JSON to remove in the end
    results = results.split("\"")
    for result in results:  # removing unwanted results
        if not result.startswith(query):
            results.remove(result)
    results = list(set(results))  # removing duplicates
    return results


class Search(DefaultRequest):
    def __init__(self, innertube_api, innertube_context, query, headers):
        self.query = query
        self.url = Urls.YOUTUBE_SEARCH.format(innertube_api)
        
        innertube_context.update({"query": query})
        self.innertube_context = innertube_context
        headers["Content-Type"] = "application/json"
        
        super().__init__(url=self.url, headers=headers)

    def search(self):
        self.post_data = json.dumps(self.innertube_context).encode()
        self.make_request(post=True)
        self.convert_json()

    def get_primary_contents(self):
        if self.result is None:
            raise exceptions.ResultIsEmpty()
        return self.result["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]

    def get_next_search_result(self, size=0):
        """
        This method fetches the next search result (generator), and-
        receives a json and formats it in the following way:
            {video id, 
             title, 
             profile picture URL, 
             channel name, 
             date published (if its not a live video),
             views count (if its a live video, it will fetch the count of watching),
             is live (if its a live video),
             video thumbnail,
             moving thumbnail (preview. only on non live videos,
             short metadata/description}
        :yield: dict
        """
        primary = self.get_primary_contents()
        results = primary["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]
        for result in results[:-2]:
            try:
                result = result["videoRenderer"]
            except KeyError:  # if its not a search result, but a "shelf" result. shelf is the results on the left side for example albums
                continue
            result_dict = {}
            result_dict["videoid"] = result["videoId"]
            result_dict["title"] = result["title"]["runs"][0]["text"]
            result_dict["pfp_url"] = result["channelThumbnailSupportedRenderers"]["channelThumbnailWithLinkRenderer"]["thumbnail"]["thumbnails"][0]["url"]
            result_dict["name"] = result["ownerText"]["runs"][0]["text"]
            if "publishedTimeText" in result.keys():  # a live video
                result_dict["date"] = result["publishedTimeText"]["simpleText"]
            if "shortViewCountText" in result.keys():
                if "simpleText" in result["shortViewCountText"].keys():
                    result_dict["views"] = result["shortViewCountText"]["simpleText"]
                else:
                    result_dict["views"] = result["shortViewCountText"]["runs"][0]["text"]
            else:
                result_dict["is_live"] = True 
                result_dict["views"] = result["viewCountText"]["runs"][0]["text"]
            if size > 1:
                raise exceptions.InvalidSize()
            result_dict["thumbnail"] = result["thumbnail"]["thumbnails"][size]["url"]
            if "richThumbnail" in result.keys():
                result_dict["moving_thumbnail"] = result["richThumbnail"]["movingThumbnailRenderer"]["movingThumbnailDetails"]["thumbnails"][0]["url"]
            if "lengthText" in result.keys():
                result_dict["length"] = result["lengthText"]["simpleText"]
            if "detailedMetadataSnippets" in result.keys():
                small_description = result["detailedMetadataSnippets"][0]["snippetText"]["runs"]
                result_dict["small_description"] = ""
                for part in small_description:
                    result_dict["small_description"] += part["text"]
            yield result_dict

    def get_continuation_token(self):
        return self.get_primary_contents()["sectionListRenderer"]["contents"][1]["continuationItemRenderer"]["continuationEndpoint"]["continuationCommand"]["token"]

    def get_more_results(self):
        self.innertube_context["continuation"] = self.get_continuation_token()
        self.make_request(post=True)
        self.convert_json()

