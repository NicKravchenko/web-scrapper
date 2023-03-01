import requests
from bs4 import BeautifulSoup
import io, json
from helper_functions import readFile, writeFile

base_url = "https://www.webometrics.info/en/WORLD?page="

universities_world = readFile("data/universities_world.json")


try:
    for i in range(0, 1, 1):  # 120
        url = base_url + str(i)
        print(url)
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")

            for table in soup.find_all("table"):
                for a in soup.find_all("a"):
                    print(a.prettify())

                # for a in soup.find_all("a"):
                #     href = str(a.get("href"))
                #     title = str(a.text)
                #     if href[:4] != "http" or href == "https://openweb.cc/":
                #         continue

                #     universities_world[title] = href
                #     print(title, href)

        else:
            print("Error: Could not fetch content")

except Exception as e:
    # writeFile("data/universities_world.json", universities_world)
    print(e)

# writeFile("data/universities_world.json", universities_world)
