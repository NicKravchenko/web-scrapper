from bs4 import BeautifulSoup
import requests
from helper_functions import readFile, writeFile, cleanify_soup_text, bcolors
import os
import urllib.parse

__dir__ = os.path.dirname(os.path.abspath(__file__))


abs_all_links = __dir__ + "/data/universities_world.json"
uni_links = readFile(abs_all_links)


def getHtml(url, session):
    url = urllib.parse.quote(url, safe=":/")

    try:
        response = session.get(url, timeout=10)
    except requests.exceptions.RequestException:
        pass

    if not response or response.status_code != 200:
        print(bcolors.FAIL + "Error on consuming: " + url + bcolors.ENDC)
        return
    print(response.text)
    return response.text


def extract_data_from_page(page):
    soup = BeautifulSoup(page, "html.parser")
    # title = soup.title.string
    # text = cleanify_soup_text(soup)
    headings = [
        heading.text
        for heading in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
    ]
    text = soup.get_text()

    print(headings)
    print(text)

    # return title, text


def process_data(data_part, session):
    for data in data_part:
        page = getHtml(data, session)

        extract_data_from_page(page)
