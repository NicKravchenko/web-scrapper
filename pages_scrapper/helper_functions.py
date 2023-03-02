import json, re


def readFile(route):
    fileObject = open(route, "r")
    jsonContent = fileObject.read()
    readed = json.loads(jsonContent)
    fileObject.close()
    return readed


def writeFile(route, content):
    jsonString = json.dumps(content)

    jsonFile = open(route, "w")
    jsonFile.write(jsonString)

    jsonFile.close()


def return_clean_link(url) -> str:
    if url[:7] == "http://":
        return url[7:]
    if url[:8] == "https://":
        return url[8:]

    return url


def cleanify_soup_text(soup_text) -> str:
    page_text = " ".join(str(soup_text.get_text()).split())
    split_text = re.findall(r"\b\w+\b", str(page_text))
    return " ".join(split_text)


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


not_allowed_links = [
    "google",
    "facebook",
    "twitter",
    "linkedin",
    "pinterest",
    "instagram",
    "youtube",
    "tumblr",
    "reddit",
    "snapchat",
    "tiktok",
    "quora",
    "medium",
    "github",
    "stackoverflow",
    "wordpress",
    "blogger",
    "wikipedia",
    "imdb",
    "yahoo",
    "amazon",
    "ebay",
    "walmart",
    "craigslist",
    "etsy",
    "homedepot",
    "lowes",
    "wayfair",
    "groupon",
    "groupon",
    "expedia",
    "booking",
    "airbnb",
    "tripadvisor",
    "kayak",
    "hotels",
    "zillow",
    "trulia",
    "realtor",
    "redfin",
    "zappos",
    "nordstrom",
    "macys",
    "sephora",
    "ulta",
    "cvs",
    "walgreens",
    "bestbuy",
    "newegg",
    "cnet",
    "pcmag",
    "techradar",
    "engadget",
    "wired",
    "gizmodo",
    "slashdot",
    "arstechnica",
    "venturebeat",
    "mashable",
    "theverge",
    "nytimes",
    "cnn",
    "bbc",
    "reuters",
    "npr",
    "abcnews",
    "usatoday",
    "foxnews",
    "huffpost",
    "buzzfeed",
    "tmz",
    "variety",
    "hollywoodreporter",
    "ign",
    "gamespot",
    "kotaku",
    "polygon",
    "rockpapershotgun",
    "youtube",
    "netflix",
    "hulu",
    "vimeo",
    "dailymotion",
    "twitch",
    "soundcloud",
    "spotify",
    "pandora",
    "iheart",
    "lastfm",
    "billboard",
    "rollingstone",
    "imslp",
    "allmusic",
    "genius",
    "pitchfork",
    "stereogum",
    "bbcgoodfood",
    "foodnetwork",
    "seriouseats",
    "allrecipes",
    "epicurious",
    "microsoft",
    "twitter",
    "youtube",
    "google",
    "instagram",
    "facebook",
    "apple",
    "mozila",
    "flickr",
    "itunes",
    "icloud",
    "edge",
    "safari",
    "outlook",
    "linkedin",
    "github",
    "wikipedia",
    "wordpress",
    "tumblr",
    "pinterest",
    "vimeo",
    "foursquare",
    "twitch",
    "slack",
    "dropbox",
    "skype",
    "whatsapp",
    "telegram",
    "snapchat",
    "spotify",
    "soundcloud",
    "tiktok",
    "reddit",
    "quora",
    "stackoverflow",
    "netflix",
    "hulu",
    "disney",
    "amazon",
    "ebay",
    "paypal",
    "walmart",
    "target",
    "craigslist",
]
