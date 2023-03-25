import requests
import urllib.parse

from bs4 import BeautifulSoup
import os
import multiprocessing
from helper_functions import (
    readFile,
    writeFile,
    bcolors,
    not_allowed_links,
    remove_special_chars,
)
from data_extractor import process_data as process_data_pages_extractor

MAX_PER_UNI = 500
MAX_RECURTION_DEPTH = 1
NUMBER_PROCESS = 1
LOWER_ARRAY_ELEMENT = 0
HIGHER_ARRAY_ELEMENT = 11
# cert_path = "/etc/ssl/certs/ca-certificates.crt"
cert_path = "C:/Users/nickr/AppData/Local/Programs/Python/Python311/lib/site-packages/certifi/cacert.pem"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    + "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Referer": "https://www.google.com/",
}


__dir__ = os.path.dirname(os.path.abspath(__file__))


abs_all_links = __dir__ + "/data/links/"
# abs_domis = __dir__ + "/data/universities_rd.json"
# uni_links = readFile(abs_all_links)

abs_unis_all_links = __dir__ + "/data/unis_all_links.json"
unis_all_links = readFile(abs_unis_all_links)

abs_links_folder = __dir__ + "/data/links/"


def get_links(
    base_url,
    detail_url,
    session,
    unis_all_links,
    recursion_depth,
    uni_file_path,
):
    """Get rid of http or https"""
    response = None
    uni = readFile(uni_file_path)
    if ("http://" in detail_url) or ("https://" in detail_url):
        url = detail_url
    else:
        url = base_url + detail_url

    url = urllib.parse.quote(url, safe=":/")

    try:
        response = session.get(url, timeout=10)
    except requests.exceptions.RequestException:
        pass

    if not response or response.status_code != 200:
        print(bcolors.FAIL + "Error on consuming: " + url + bcolors.ENDC)
        return
    soup = BeautifulSoup(response.content, "html.parser")

    for a in soup.find_all("a"):
        href = str(a.get("href"))
        """Add href only if its relative path or it contains name of page"""
        if not (href[:1] == "/" or ("http://" in href) or ("https://" in href)) or (
            any(ext in href for ext in not_allowed_links)
        ):
            continue

        composed_url = base_url + href

        if base_url[-1] == "/":
            if href[0] == "/":
                href = href[1:]
                composed_url = base_url + href

        if ("http://" in href) or ("https://" in href):
            composed_url = href

        composed_url = urllib.parse.quote(composed_url, safe=":/")

        try:
            response_check_if_404 = session.get(composed_url, timeout=20)
        except requests.exceptions.RequestException:
            continue

        if (composed_url in uni[base_url]) or (
            not response_check_if_404 or response_check_if_404.status_code == 404
        ):
            print(
                bcolors.WARNING
                + "Skipped recursivamente With Base: "
                + base_url
                + " Detail : "
                + detail_url
                + bcolors.ENDC
            )
            continue

        uni[base_url].append(composed_url)

        writeFile(uni_file_path, uni)
        print(bcolors.OKGREEN + "Was saved " + composed_url + bcolors.ENDC)

        print("Amount: " + str(len(uni[base_url])) + " depth " + str(recursion_depth))

        if (len(uni[base_url]) > MAX_PER_UNI) or (
            recursion_depth > MAX_RECURTION_DEPTH
        ):
            continue

        get_links(
            base_url,
            href,
            session,
            unis_all_links,
            recursion_depth + 1,
            uni_file_path,
        )


def process_data(universities_links):
    for uni in universities_links:
        """Start session for retrieving one domain"""
        uni = remove_special_chars(uni)
        session = requests.Session()
        session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                + "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
                "Referer": "https://www.google.com/",
            }
        )
        session.verify = cert_path
        session.adapters.DEFAULT_RETRIES = 3
        try:
            base_url = uni_links[uni]
            # base_url = "https://www.intec.edu.do"
            if base_url not in unis_all_links:
                unis_all_links[base_url] = []

            uni_file_path = abs_links_folder + f"/{uni}.json"
            try:
                fileObject = open(uni_file_path, "x")
                fileObject.close()
            except Exception as e:
                print("File already exists")
                print("Error on open file")
                print(e)

            if os.path.getsize(uni_file_path) == 0:
                with open(uni_file_path, "w") as file:
                    file.write('{ "' + base_url + '" : [] }')
                    file.close()

            base_url = uni_links[uni]

            get_links(base_url, "", session, unis_all_links, 0, uni_file_path)

            print("Finished with " + base_url)

        except Exception as e:
            print("Closed with error:")
            print(e)
            e.with_traceback(None)
            print(arg for arg in e.args)

            pass


def runLinkScrapper():
    num_processes = NUMBER_PROCESS

    unis_to_use = {
        k: uni_links[k]
        for k in list(uni_links)[LOWER_ARRAY_ELEMENT:HIGHER_ARRAY_ELEMENT]
    }

    data_parts = [list(unis_to_use)[i::num_processes] for i in range(num_processes)]

    processes = []
    for i, data_part in enumerate(data_parts):
        p = multiprocessing.Process(target=process_data, args=(data_part,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()


def runDataExtractor():
    num_processes = 1
    link_counter = 0
    file_name = 1

    for filename in os.listdir(abs_links_folder):
        if not filename.endswith(".json"):
            continue

        data = readFile(abs_links_folder + filename)

        try:
            # Convert the dictionary into a list and access the array using its index position
            array_index = 0  # Set the index position of the array
            unis_to_use = list(data.values())[array_index]
        except Exception as e:
            print("Error:")
            print(e)
            continue

        # for i in list(array):
        session = requests.Session()
        session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                + "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
                "Referer": "https://www.google.com/",
            }
        )
        session.verify = cert_path
        session.adapters.DEFAULT_RETRIES = 3

        # print(i)
        link_counter += len(unis_to_use)
        if link_counter > 800:
            file_name += 1
            link_counter = 0

        data_parts = [list(unis_to_use)[i::num_processes] for i in range(num_processes)]

        processes = []
        for i, data_part in enumerate(data_parts):
            p = multiprocessing.Process(
                target=process_data_pages_extractor,
                args=(data_part, session, file_name),
            )

            processes.append(p)
            p.start()

        for p in processes:
            p.join()


if __name__ == "__main__":
    runDataExtractor()
    # runLinkScrapper()
