import requests
import urllib.parse

from bs4 import BeautifulSoup
import io, json, os, sys
from helper_functions import (
    readFile,
    writeFile,
    return_clean_link,
    cleanify_soup_text,
    bcolors,
    not_allowed_links,
)

MAX_PER_UNI = 1000
MAX_RECURTION_DEPTH = 20
# data_intec_json = "data/intec.json"
# absolute_path_intec_json = os.path.abspath(data_intec_json)

# intec_json = readFile("data/intec.json")

cert_path = "/etc/ssl/certs/ca-certificates.crt"
# cert_path = "C:/Users/Nikita/AppData/Local/Programs/Python/Python311/lib/site-packages/certifi/cacert.pem"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Referer": "https://www.google.com/",
}

relat_all_links = "data/universities_world.json"
unis_all_links = os.path.abspath(relat_all_links)
uni_links = readFile(unis_all_links)

relat_unis_all_links = "data/unis_all_links.json"
unis_unis_all_links = os.path.abspath(relat_unis_all_links)
unis_all_links = readFile(unis_unis_all_links)


def get_links(base_url, detail_url, session, unis_all_links, recursion_depth):
    """Get rid of http or https"""
    response = None

    if ("http://" in detail_url) or ("https://" in detail_url):
        url = detail_url
    else:
        url = base_url + detail_url

    url = urllib.parse.quote(url, safe=":/")

    url_no_http = return_clean_link(url)

    try:
        response = session.get(url, timeout=10)
        # Process the response here...
    except requests.exceptions.RequestException:
        # Ignore any errors and continue to the next URL
        pass

    if not response or response.status_code != 200:
        print(bcolors.FAIL + "Error on consuming: " + url + bcolors.ENDC)
        return
    soup = BeautifulSoup(response.content, "html.parser")

    for a in soup.find_all("a"):
        href = str(a.get("href"))
        """Add href only if its relative path or it contains name of page"""
        if not (
            href[:1] == "/" or ("http://" in href) or ("https://" in href)
        ) or (any(ext in href for ext in not_allowed_links)):
            continue

        composed_url = base_url + href

        if base_url[-1] == "/":
            if href[0] == "/":
                href = href[1:]
                composed_url = base_url + href

        if ("http://" in href) or ("https://" in href):
            composed_url = href

        composed_url = urllib.parse.quote(composed_url, safe=":/")

        response_check_if_404 = session.get(composed_url, timeout=20)

        if (composed_url in unis_all_links[base_url]) or (
            not response_check_if_404
            or response_check_if_404.status_code == 404
        ):
            print(
                bcolors.WARNING
                + "Skipped recursivamente With Base: "
                + base_url
                + " Detail : "
                + detail_url
                + bcolors.ENDC
            )
            # get_links(base_url, href, session, unis_all_links)
            continue

        unis_all_links[base_url].append(composed_url)

        writeFile("data/unis_all_links.json", unis_all_links)
        print(bcolors.OKGREEN + "Was saved " + composed_url + bcolors.ENDC)
        print(
            "Amount: "
            + str(len(unis_all_links[base_url]))
            + " depth "
            + str(recursion_depth)
        )
        if (len(unis_all_links[base_url]) > MAX_PER_UNI) or (
            recursion_depth > MAX_RECURTION_DEPTH
        ):
            continue
        get_links(base_url, href, session, unis_all_links, recursion_depth + 1)


def decompose_page(url, session):
    hList = {}
    page_text = ""

    """Get rid of http or https"""
    url_no_http = return_clean_link(url)

    response = session.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        text = cleanify_soup_text(soup)

        for a in soup.find_all("a"):
            href = str(a.get("href"))
            """Add href only if its relative path or it contains name of page"""
            if href[:1] == "/":  # or (url_no_http in href):
                links.append(href)

        for i in range(1, 7):
            hList[i] = []
            for h in soup.find_all(f"h{i}"):
                hList[i].append(h.text)

        # intec_json[url] = {}
        # intec_json[url]["header"] = hList

        # intec_json[url]["body"] = text

        # print(text)
        # print(intec_json)
        # print(links)


try:
    """Start session for retrieving one domain"""
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "Referer": "https://www.google.com/",
        }
    )
    session.verify = cert_path

    session.adapters.DEFAULT_RETRIES = 3

    for uni in uni_links:
        # base_url = uni_links[uni]
        base_url = "https://www.intec.edu.do"
        # base_url = "https://aab-edu.net/"
        if base_url not in unis_all_links:
            unis_all_links[base_url] = []

        get_links(base_url, "", session, unis_all_links, 0)
        writeFile("data/unis_all_links.json", unis_all_links)

        print("Finished with " + base_url)

        break


except Exception as e:
    print("Closed with error:")
    print(e)
    e.with_traceback(None)
    print(arg for arg in e.args)

    pass
