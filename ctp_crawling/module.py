import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from collections import defaultdict as dd
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
from tqdm import tqdm

img2tier = {"0.svg": "Unrated",
            "1.svg": "Bronze V",
            "2.svg": "Bronze IV",
            "3.svg": "Bronze III",
            "4.svg": "Bronze II",
            "5.svg": "Bronze I",
            "6.svg": "Silver V",
            "7.svg": "Silver IV",
            "8.svg": "Silver III",
            "9.svg": "Silver II",
            "10.svg": "Silver I",
            "11.svg": "Gold V",
            "12.svg": "Gold IV",
            "13.svg": "Gold III",
            "14.svg": "Gold II",
            "15.svg": "Gold I",
            "16.svg": "Platinum V",
            "17.svg": "Platinum IV",
            "18.svg": "Platinum III",
            "19.svg": "Platinum II",
            "20.svg": "Platinum I",
            "21.svg": "Diamond V",
            "22.svg": "Diamond IV",
            "23.svg": "Diamond III",
            "24.svg": "Diamond II",
            "25.svg": "Diamond I",
            "26.svg": "Ruby V",
            "27.svg": "Ruby IV",
            "28.svg": "Ruby III",
            "29.svg": "Ruby II",
            "30.svg": "Ruby I"}

target = {"Bronze": ("Sprout", "Bronze"),
          "Silver": ("Bronze", "Silver"),
          "Gold": ("Bronze", "Gold"),
          "Platinum": ("Gold", "Platinum"),
          "Diamond": ("Platinum", "Diamond"),
          "Ruby": ("Diamond", "Ruby")}

class Crawling:
    __boj_handle = ""
    __date = ""
    __driver = None
    __tier = ""
    __start_date = ()
    __end_date = ()
    __solved_problem = dd(str)
    __proper_problem = dd(str)
    __improper_problem = dd(str)

    def __init__(self, boj_handle: str, date: str, driver):
        self.__boj_handle = boj_handle
        self.__driver = driver
        self.__date = date

        self.__get_tier()
        self.__set_date()
        self.__seperate_solved_problem()

    def __get_tier(self):
        global img2tier

        self.__driver.get(f"https://www.acmicpc.net/user/{self.__boj_handle}")

        src = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[3]/div[1]/div/h1/a/img').get_attribute('src')
        tier_img = src.split('/')[-1]
        self.__tier = img2tier[tier_img]

    def __get_recent_solved_problem(self):
        self.__driver.get(f"https://www.acmicpc.net/status?problem_id=&user_id={self.__boj_handle}&language_id=-1&result_id=4")

        tbody = self.__driver.find_element(By.XPATH, '//*[@id="status-table"]/tbody')
        rows = tbody.find_elements(By.TAG_NAME, "tr")

        for row in rows:
            problem = row.find_elements(By.TAG_NAME, "td")[2]
            date = row.find_elements(By.TAG_NAME, "td")[8].find_element(By.TAG_NAME, "a").get_attribute("data-original-title")
            self.__solved_problem[problem.text] = date

    def __get_problem_tier(self, problem: str) -> str:
        self.__driver.get("https://solved.ac/search")

        search = self.__driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/div[1]/input')
        search.send_keys(problem)
        search.send_keys(Keys.ENTER)
        tier = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div[2]/div[2]/table/tbody/tr/td[1]/div/div/div/span/a/img').get_attribute('alt')

        return tier

    def __parse_date(self, date: str) -> tuple:
        """
        parsing date with the following format
        (year, month, day, hour_with_24_format, minute, second)

        for example, 2023년 3월 21일 19:13:29 becomes (2023, 3, 21, 19, 13, 29)
        """
        y, m, d, t = date.split()
        y, m, d = int(y[:-1]), int(m[:-1]), int(d[:-1])
        ret = (y, m, d, *map(lambda x: int(x), t.split(':')))

        return ret

    def __set_date(self):
        """
        set __start_date and __end_date with the following format
        (year, month, day, hour_with_24_format, minute, second)
        """
        yesterday = datetime.now() - timedelta(days=1)
        self.__start_date = (yesterday.year, yesterday.month, yesterday.day, 5, 0, 0)

        today = datetime.now()
        self.__end_date = (today.year, today.month, today.day, 5, 0, 0)

    def __is_valid_tier(self, problem) -> bool:
        """
        verdict one solved the valid tier problem
        Here, valid problem means tier between solver tier and one level below

        for example, if solver's tier is gold 3
        then, he must solve between gold and silver problem
        """
        global target

        print(problem)
        problem_tier = self.__get_problem_tier(problem).split()[0]
        tier = self.__tier.split()[0]

        return True if tier in target[problem_tier] else False

    def __is_valid_date(self, solved_date):
        solved_date = self.__parse_date(solved_date)

        return True if self.__start_date <= solved_date <= self.__end_date else False

    def __seperate_solved_problem(self):
        self.__get_recent_solved_problem()

        # for problem, solved_date in self.__solved_problem.items():
        #     if self.__is_valid_tier(problem) and self.__is_valid_date(solved_date):
        #         self.__proper_problem[problem] = solved_date
        #     else: self.__improper_problem[problem] = solved_date

    def removethis(self):
        print(self.__solved_problem)
        print(self.__proper_problem)
        print(self.__improper_problem)

    def get_problem_tier(self, problem: str) -> str:
        self.__driver.get("https://solved.ac/search")

        search = self.__driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[1]/input')
        search.send_keys(problem)
        search.send_keys(Keys.ENTER)
        tier = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div[2]/div[2]/table/tbody/tr/td[1]/div/div/div/span/a/img').get_attribute('alt')

        return tier


def init():
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(time_to_wait=5)
    return driver

def get_class_list(c : str) -> list:
    df = pd.read_excel("23_enrollment_info.xlsx")
    return df.loc[df[c] == 'O']

if __name__ == "__main__":
    driver = init()

    tmp = Crawling(boj_handle="jinik9903", date="2023 3월 4일", driver = driver)
    # tmp.removethis()
    tmp.get_problem_tier("10872")

    driver.quit()