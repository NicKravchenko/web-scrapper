import requests
from bs4 import BeautifulSoup
import re

base_url = "https://en.wikipedia.org/"

detail_url = "wiki/Lists_of_universities_and_colleges_by_country"

url = base_url + detail_url

response = requests.get(url)
universities = {}
if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    for link in soup.find_all("a"):
        a = link.get("href")
        title = link.get("title")

        # print("Link: " + str(link))
        # print("a: " + str(a))
        # print("title: " + str(title))

        if str(a).startswith("/wiki") and str(title).startswith(
            "List of universities in"
        ):
            university = str(title).replace("List of universities in ", "")
            universities[university] = base_url + a

            # print(university + " - " + base_url + a)

    print(universities)
    # print(link.get("href"))
    # print(soup.prettify())
    # print(response.content)
else:
    print("Error: Could not fetch content")
