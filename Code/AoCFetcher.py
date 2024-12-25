import re
import requests
from bs4 import BeautifulSoup


def fetch_problem(year, day, session_cookie):
    url = f"https://adventofcode.com/{year}/day/{day}"
    cookies = {'session': session_cookie}
    response = requests.get(url, cookies=cookies)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        parts = soup.find_all('article')

        while len(parts) < 2:
            parts.append("Could not fetch Part 2")

        return [part.text if hasattr(part, 'text') else part for part in parts[:2]]
    else:
        print(f"Failed to fetch problem for {year} day {day}.")
        return ["Could not fetch Part 1", "Could not fetch Part 2"]


def extract_last_sentence(text):
    sentences = re.split(r'(?<=[.!?]) +', text.strip())
    return sentences[-1] if sentences else "No hint available."
