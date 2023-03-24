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
    response = None
    try:
        response = session.get(url, timeout=10)
    except requests.exceptions.RequestException:
        pass

    if not response or response.status_code != 200:
        print(bcolors.FAIL + "Error on consuming: " + url + bcolors.ENDC)
        return
    return response.text


def extract_data_from_page(page):
    try:
        soup = BeautifulSoup(page, "html.parser")
        # title = soup.title.string
        # text = cleanify_soup_text(soup)
        title = soup.title.string if soup.title else "No title"

        headings = [
            heading.text for heading in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
        ]
        # text = soup.text
        text = cleanify_soup_text(soup)

        return title, headings, text
        # return title, text
    except Exception as e:
        print("Error on extracting data from page")
        print(e)
        return "None", ["None"], "None"


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
            file.write("{ }")
            file.close()


def addPage(route, file, url, title, headings, text):
    file[url] = {
        "title": title,
        "headings": headings,
        "body": text,
    }
    # file[url]["headings"] = headings
    writeFile(route, file)
    print(file)


def process_data(data_part, session):
    a = 1
    current_a = a
    base_route = __dir__ + f"/data/pages_content/"
    route = base_route + str(a) + ".json"
    file = None

    for url in data_part:
        if a == 1 or a % 200 == 0:
            fileName = str(a) + ".json"
            createFile(fileName)
            current_a = a
            route = base_route + fileName
            file = readFile(route)
        a += 1

        if url in file:
            print("Site is there")
            continue

        page = getHtml(url, session)
        title, headings, text = extract_data_from_page(page)
        addPage(route, file, url, title, headings, text)
