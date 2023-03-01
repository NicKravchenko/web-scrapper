import requests
from bs4 import BeautifulSoup
import io, json, os, sys
from helper_functions import (
    readFile,
    writeFile,
    return_clean_link,
    cleanify_soup_text,
)


intec_json = readFile("data/intec.json")

cert_path = "C:/Users/Nikita/AppData/Local/Programs/Python/Python311/lib/site-packages/certifi/cacert.pem"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Referer": "https://www.google.com/",
}

uni_links = readFile("data/universities_world.json")

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
        # url = uni_links[uni]
        # print(uni)
        # url = "https://github.com/4teamwork/ftw.linkchecker/issues/57"
        # url = "http://www.intec.edu.do/"
        url = "http://www.au.edu.az/"

        links = []
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
                if href[:1] == "/" or (url_no_http in href):
                    links.append(href)

            for i in range(1, 7):
                hList[i] = []
                for h in soup.find_all(f"h{i}"):
                    hList[i].append(h.text)

            intec_json[url] = {}
            intec_json[url]["header"] = hList

            intec_json[url]["body"] = text

            # print(text)
            print(intec_json)
            # print(links)

            writeFile("data/intec.json", intec_json)

        break


except Exception as e:
    print(e)


# writeFile("data/intec.json", intec_json)


# response = requests.get(
#     url,
#     # verify=False
#     verify=cert_path,
#     headers=headers,
# )
