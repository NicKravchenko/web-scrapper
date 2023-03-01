import requests
from bs4 import BeautifulSoup
import io, json
from helper_functions import readFile, writeFile


universities_links_wiki = readFile("data/universities_links.json")
universities_links = readFile("data/universities_orig_links.json")

for key in universities_links_wiki:
    countryOfUnis = universities_links_wiki[key]
    universitiesOfCountry = {}

    for key in countryOfUnis:
        url = countryOfUnis[key]
        print("Uni:")
        print(url)

        if url.count("://") > 1:
            print("More than one ://")
            break

        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")

            for table in soup.find_all("table", {"class": "infobox vcard"}):
                for tr in table.find_all("tr"):
                    for th in tr.find_all("th"):
                        if "Website" not in th.text:
                            break
                        for a in tr.find_all("a"):
                            href = str(a.get("href"))
                            print(href)
                            universities_links[key] = href
        print("--------------------")


# print(universities_links)

writeFile("data/universities_orig_links.json", universities_links)
