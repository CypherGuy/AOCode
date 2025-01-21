from bs4 import BeautifulSoup
import subprocess
import time
import tempfile

import requests


def execute_code(code):
    start_time = time.time()
    try:
        if len(code) == 0:
            return "Nothing in the terminal to execute :()"
        with tempfile.NamedTemporaryFile('w', suffix='.py') as f:
            f.write(code)
            f.flush()
            result = subprocess.run(['python', f.name], stdin=subprocess.PIPE, capture_output=True,
                                    text=True, timeout=20, encoding='utf-8')
            # I included stdin=subprocess.PIPE as the user may want to request inputs, however
            # unlikely. Additionally AoC solutions can all be done in under 15 seconds so I give
            # a bit of leeway just in case.
            if result.returncode == 0:
                return result.stdout
            else:
                end_time = time.time()
                time_taken = end_time - start_time
                return f"Process took approximately {time_taken:.4f} seconds\n{result.stderr}"
    except subprocess.TimeoutExpired:
        return "There's very likely an infinite loop/recursion or a way to do it much quicker. Every solution can be done in under 15 seconds, this has returned after 60."


def submit_answer(year, day, part, token, answer, terminal):
    url = f"https://adventofcode.com/{year}/day/{day}/answer"
    headers = {
        'User-Agent': 'AoCode',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'level': part,
        'answer': answer,
    }
    cookies = {
        'session': token,
    }

    response = requests.post(url, headers=headers, data=data, cookies=cookies)

    # Parse the response.text using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    p_tag = soup.find('article').find('p')

    for a_tag in p_tag.find_all('a'):
        a_tag.decompose()

    # Locate the specific <p> tag within the <article>
    article_text = p_tag.text.strip()

    if "That's the right answer" in article_text:
        x = "Answer submitted successfully! That's the right answer."
    elif "That's not the right answer" in article_text:
        x = article_text
    elif "You gave an answer too recently" in article_text:
        x = article_text
    else:
        x = "Answer submitted, received unexpected response."

    # Determine the colour based on success or failure
    colour = "green" if "Answer submitted successfully! That's the right answer." in article_text else "red"

    # Append the styled text to the terminal
    terminal.append(f'''<span style="color: {
        colour};">------<br>{x}</span>''')
    print(x)
