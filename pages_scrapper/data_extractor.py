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
    return response.text


def extract_data_from_page(page):
    soup = BeautifulSoup(page, "html.parser")
    # title = soup.title.string
    # text = cleanify_soup_text(soup)
    headings = [
        heading.text
        for heading in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
    ]
    # text = soup.text
    text = cleanify_soup_text(soup)


    return headings, text
    # return title, text

def createFile(name):
    loc = __dir__ + f"/data/pages_content/{name}"

    try:
        fileObject = open(loc, "x")
        fileObject.close()
    except Exception as e:
        print("File already exists")
        print("Error on open file")
        print(e)

    if os.path.getsize(loc) == 0:
        with open(loc, "w") as file:
            file.write('{ }')
            file.close()

def addPage(route, file, url, headings, text):
    file[url] = {
        "headings" : headings,
        "body" : text,
    }
    # file[url]["headings"] = headings
    writeFile(route, file)
    print(file)


def process_data(data_part, session):
    a = 1
    current_a = a
    base_route = __dir__ + f"/data/pages_content/"
    route = base_route + str(a)

    for url in data_part:
        current_a = a
        if a==1 or a % 200==0:
            createFile(a)
            current_a = a
            route = base_route + str(a)
            file = readFile(route)
        a += 1

        page = getHtml(url, session)

        headings, text = extract_data_from_page(page)

        addPage(route, file, url, headings, text)
