import os
import requests
from bs4 import BeautifulSoup
import crawling_info as ci
from tqdm import tqdm

def parsing_question(url):
    ret = dict()

    headers = {"User-Agent": ci.INFO["User-Agent"]}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    title = soup.find("span", {"id": "problem_title"}).get_text()
    ret.update({"title": title})
    ret.update({"url": url})

    return ret

def create_source(db, keystarter='<'):
    """ Programmatically create ktx file with the questions (and hints and solutions if required)
    saved under source files """

    with open("../source/exercises100.ktx", "w+") as f:
        for ind, url in tqdm(enumerate(db, 1)):
            data = parsing_question(url)
            f.write(f"{keystarter} q{ind}\n")
            f.write(f"[{data['title']}]({data['url']})\n\n")

            f.write(f"{keystarter} h{ind}\n")
            f.write(f"hint: \n\n")

            f.write(f"{keystarter} a{ind}\n")
            f.write("\n\n")

db = ci.load_problem_url()
create_source(db)