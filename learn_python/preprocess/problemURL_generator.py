import os
import requests
from bs4 import BeautifulSoup
import crawling_info as ci

def parsing_question(url):
    global db

    headers = {"User-Agent": ci.INFO["User-Agent"]}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    for anchor in soup.findAll('a', href=True):
        curUrl = anchor['href']
        if "problem" in curUrl: db.add(curUrl)

parseList = ["https://code.plus/course/41",
             "https://code.plus/course/42"]
db = ci.load_problem_url()
for url in parseList: parsing_question(url)

with open("../source/problemURL.ktx", 'r+') as f:
    for data in sorted(db): f.write(data.strip()+"\n")