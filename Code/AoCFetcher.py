import re
import requests


def fetch_problem(year, day, session_cookie):
    url = f"https://adventofcode.com/{year}/day/{day}"
    cookies = {'session': session_cookie}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }
    response = requests.get(url, cookies=cookies, headers=headers)

    if response.status_code == 200:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        parts = soup.find_all('article')

        while len(parts) < 2:
            parts.append("Could not fetch Part 2. Maybe it's locked?")

        return [part.text if hasattr(part, 'text') else part for part in parts[:2]]
    else:
        print(f"Failed to fetch problem for {year} day {day}.")
        return ["Could not fetch Part 1. Maybe it's locked?", "Could not fetch Part 2. Maybe it's locked?"]


def fetch_input(year, day, session_cookie=None):
    if session_cookie is None:
        session_cookie = input("Enter your session cookie: ")

    url = f"https://adventofcode.com/{year}/day/{day}/input"
    session = requests.Session()

    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    })

    session.cookies.set('session', session_cookie, domain='adventofcode.com')
    response = session.get(url)
    print(response.status_code)

    if response.status_code == 200:
        return response.text
    else:
        return f"Failed to fetch input for {year} day {day}. Maybe your session key is wrong?"


def get_last_paragraph(text):
    paragraphs = [p for p in text.split('\n') if p.strip()]
    return paragraphs[-1] if paragraphs else ''
