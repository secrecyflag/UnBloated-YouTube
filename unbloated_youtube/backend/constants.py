import enum


class Common:
    VAR_YTCONFIG = "var ytInitialPlayerResponse"
    VAR_YTDATA = "var ytInitialData"
    STREAMINGDATA = "streamingData"
    ADAPTIVEFORMATS = "adaptiveFormats"
    DURATION = "approxDurationMs"
    SECONDS = "sec"
    MINUTES = "min"
    # 5KB, used to load video buffer can be any bytes size, but it will take longer to load
    RANDOM_RANGE = 524288 
    YOUTUBE_URL = "https://www.youtube.com"
    YOUTUBE_NEXT_URL = YOUTUBE_URL + "/youtubei/v1/next?key={0}"


class Urls:
    YOUTUBE_URL = "https://www.youtube.com"
    YOUTUBE_NEXT_URL = YOUTUBE_URL + "/youtubei/v1/next?key={0}"
    YOUTUBE_SEARCH = YOUTUBE_URL + "/youtubei/v1/search?key={0}"


class RePatterns:
    CONFIG_PATTERN = r"var ytInitialPlayerResponse\s?=\s?.*;</"
    CLEN_PATTERN = r"clen=[0-9]*"
    DATA_PATTERN = r"var ytInitialData\s?=\s?.*;</script"
    YTCFG_MORE = r"ytcfg\.set\(\{.*\}\);\s"
    SEARCH_RESULTS = r"\[.*]"
    SEARCH_RESULTS_SUB = r"(\[|\]|,)"
    URL = r"https://.*"
    SIGNATURE = r"(?<=(\bs=)).*?(?=&)"
    # SINGNATURE REGEX
    DECIPHER_FUNCTION = r"\b[a-zA-Z0-9]*\s*=\s*function\s*\(\s*a\s*\)\s*\{a=a\.split\(\"\"\).*\};"
    DICT_FUNCTION_NAME = r"\b[^a(?!\.)=][a-zA-Z0-9]*(?=\.)"
    @staticmethod
    def find_dict_functions(dict_function_name):
        return r"(?<=\b(var)\s(" + dict_function_name + r")={)[a-zA-Z0-9]*\s*:\s*function.*[\n|\r|\r\n]?.*[\n|\r|\r\n]?.*?(})"


class Sizes(enum.Enum):
    """
    enum to represent different sizes from youtube, 
    such as small youtube thumbnails or profile pictures.
    the sizes are different for each request, for example:
    youtube only returns 68x68 profile pictures when receiving search results,
    but when in a video you could even get 48x48. then it depends on the situation
    """
    SMALL = 0
    MEDIUM = 1
    BIG = 2

