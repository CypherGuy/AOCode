import requests
from bs4 import BeautifulSoup


from typing import List, Tuple


def fetch_problem(year: int, day: int, session_cookie: str) -> Tuple[List[str], str]:
    url = f"https://adventofcode.com/{year}/day/{day}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
               "AppleWebKit/537.36 (KHTML, like Gecko) "
               "Chrome/96.0.4664.110 Safari/537.36"
               }
    s = requests.Session()
    s.headers.update(headers)
    s.cookies.set("session", session_cookie)
    response = s.get(url)

    if response.status_code != 200:
        return ["", ""], "Could not fetch Part 1. Is it in the future?"

    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("article")

    parts = []
    for _, article in enumerate(articles):
        article_text = article.text if article.text else ""
        parts.append(article_text)

    parts = parts[:2]
    if len(parts) < 2:
        parts.append("")
    return parts, ""


def fetch_input(year: int, day: int, session_cookie: str) -> str:
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    session = requests.Session()

    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    })

    session.cookies.set('session', session_cookie, domain='adventofcode.com')
    response = session.get(url)

    if response.status_code == 200:
        return response.text
    else:
        return f"Failed to fetch input for {year} day {day}. Are you sure it's unlocked?"


def get_last_paragraph(text: str) -> str:
    paragraphs = [p for p in text.split('\n') if p.strip()]
    return paragraphs[-1] if paragraphs else ''
