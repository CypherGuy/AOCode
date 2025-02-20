import requests
from bs4 import BeautifulSoup


def fetch_problem(year, day, session_cookie):
    url = f"https://adventofcode.com/{year}/day/{day}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
               "AppleWebKit/537.36 (KHTML, like Gecko) "
               "Chrome/96.0.4664.110 Safari/537.36"
               }
    s = requests.Session()
    s.headers.update(headers)
    s.cookies.set("session", session_cookie)
    response = s.get(url)

    print(response.text)

    if response.status_code != 200:
        return ["Could not fetch Part 1. Maybe it's locked?", "Could not fetch Part 2. Maybe it's locked?"]

    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("article")

    parts = []
    for article in articles:
        if article.text:
            parts.append(article.text)
        else:
            parts.append("No Part found")

    parts = parts[:2]
    if len(parts) < 2:
        parts.append("Part 2 not unlocked yet.")
    return parts


def fetch_input(year, day, session_cookie):
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


def get_last_paragraph(text):
    paragraphs = [p for p in text.split('\n') if p.strip()]
    return paragraphs[-1] if paragraphs else ''
