import requests
from bs4 import BeautifulSoup
from collections import defaultdict as dd
import matplotlib.pyplot as plt
 
db = dd(lambda: dd(int))
cnt = dd(int)
 
for page in range(1, 71):
    print(page)
    url = f"https://codeforces.com/problemset/page/{page}?order=BY_RATING_DESC"
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    table = soup.select("table.problems > tr")
 
    for problem_info in table[1:]:
        col = problem_info.select("td")
        difficulty = col[3].get_text().split()
        if difficulty:
            difficulty = int(difficulty[0])
        else: difficulty = 0
        if(len(col[1].select("a")[1:])):
            cnt[difficulty] += 1
            for e in col[1].select("a")[1:]:
                db[difficulty][e.get_text()] += 1
 
for diff in db.keys():
    d = {k: v for k, v in sorted(db[diff].items(), key=lambda item: item[1])}
    plt.rcParams.update({'font.size': 5})
    plt.barh(range(len(d)), d.values(), align='center', color='orange')
    plt.yticks(range(len(d)), d.keys())
    plt.xlabel(f"*{diff}, total: {cnt[diff]}", fontsize=18)
    plt.ylabel(' ', fontsize=18)
 
    plt.savefig(f"{diff}.png", dpi=300)
   plt.cla()