import requests
from bs4 import BeautifulSoup


def get_champions():
    champions = []
    for idx in range(1, 4):
        content = requests.get(f"http://war3nobu.wltw.org/champion{idx}").content
        soup = BeautifulSoup(content, "lxml")
        for divs in soup.select("div.cb"):
            for div in divs.select("a"):
                champion = {}
                champion["name"] = (
                    div.select_one("div.l").text + div.select_one("div.s").text
                )
                champion["image"] = (
                    "./champions/" + div.select_one("img")["src"].split("/")[-1]
                )
                get_champions_image(
                    "https://war3nobu.wltw.org/" + div.select_one("img")["src"]
                )
                champion["discribe"] = get_skills(div["href"])
                champions.append(champion)
    return champion


def get_skills(code):
    skills = []
    for div in BeautifulSoup(
        requests.get(f"http://war3nobu.wltw.org/{code}").content, "lxml"
    ).select("div.cp_s_n")[:-1]:
        skills.append(div.text)
    return skills


def get_champions_image(url):
    headers = {
        "Referer": "http://war3nobu.wltw.org/",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
    }
    r = requests.get(url, headers=headers).content
    name = url.split("/")[-1]
    with open(f"./champions/{name}", "wb") as file:
        file.write(r)
