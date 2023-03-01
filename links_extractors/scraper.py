import requests
from bs4 import BeautifulSoup
import io, json

from helper_functions import readFile, writeFile

universities = {}

base_url = "https://en.wikipedia.org"
detail_url = "/wiki/Lists_of_universities_and_colleges_by_country"
url = base_url + detail_url


file_universities = readFile("data/universities.json")
countries = readFile("data/countries.json")

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")

    for link in soup.find_all("a"):
        href = link.get("href")
        title = link.get("title")

        if str(href).startswith("/wiki") and str(title).startswith(
            "List of universities in"
        ):
            universityTitle = str(title).replace(
                "List of universities in ", ""
            )

            if universityTitle.startswith("the "):
                universityTitle = universityTitle[4:]

            link = base_url + href

            if (
                universityTitle not in file_universities
                and universityTitle in countries.values()
            ):
                universities[universityTitle] = link

else:
    print("Error: Could not fetch content")

aDict = file_universities | universities

writeFile("data/universities.json", aDict)

print(universities)
