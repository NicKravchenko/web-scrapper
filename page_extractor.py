import requests
from bs4 import BeautifulSoup
import io, json
from helper_functions import readFile, writeFile

base_url = "https://en.wikipedia.org"


universities_links = readFile("data/universities_links.json")
universities = readFile("data/universities.json")

for key in universities:
    detail_url = universities[key]
    universitiesOfCountry = {}

    url = detail_url
    print(url)
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        for link in soup.find_all("a"):
            href = str(link.get("href"))
            title = str(link.get("title"))

            if ("university" or "universidad") in href.lower():
                universitiesOfCountry[title] = base_url + href
                print(title + " - " + href)

            # print(href)
        universities_links[key] = universitiesOfCountry
        # print(soup.prettify())
        # break

    else:
        print("Error: Could not fetch content")

writeFile("data/universities_links.json", universities_links)
# print(universities_links)
