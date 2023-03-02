import requests
from bs4 import BeautifulSoup
import io, json, os, sys
from helper_functions import (
    readFile,
    writeFile,
    return_clean_link,
    cleanify_soup_text,
    bcolors,
)

MAX_PER_UNI = 100

intec_json = readFile("data/intec.json")

cert_path = "C:/Users/Nikita/AppData/Local/Programs/Python/Python311/lib/site-packages/certifi/cacert.pem"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Referer": "https://www.google.com/",
}

uni_links = readFile("data/universities_world.json")
unis_all_links = readFile("data/unis_all_links.json")


def get_links(base_url, detail_url, session, unis_all_links):
    """Get rid of http or https"""
    response = None

    if ("http://" in detail_url) or ("https://" in detail_url):
        url = detail_url
    else:
        url = base_url + detail_url

    url_no_http = return_clean_link(url)

    try:
        response = session.get(url)
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
        ):
            continue

        composed_url = base_url + href

        if base_url[-1] == "/":
            if href[0] == "/":
                href = href[1:]
                composed_url = base_url + href

        if ("http://" in href) or ("https://" in href):
            composed_url = href

        if composed_url in unis_all_links[base_url]:
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
        print(len(unis_all_links[base_url]))
        if len(unis_all_links[base_url]) > MAX_PER_UNI:
            continue
        get_links(base_url, href, session, unis_all_links)


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

        intec_json[url] = {}
        intec_json[url]["header"] = hList

        intec_json[url]["body"] = text

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

    for uni in uni_links:
        base_url = uni_links[uni]
        # base_url = "http://www.intec.edu.do"
        if base_url not in unis_all_links:
            unis_all_links[base_url] = []

        get_links(base_url, "", session, unis_all_links)
        writeFile("data/unis_all_links.json", unis_all_links)


except Exception as e:
    print("Closed with error:")
    print(e)
    e.with_traceback(None)
    print(arg for arg in e.args)
