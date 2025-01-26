from bs4 import BeautifulSoup
import subprocess
import time
import tempfile
import requests
import config


def execute_code(code):
    utils_file = open(f"user_files/{config.HASHED_TOKEN}/utils.py", "r").read()
    start_time = time.time()
    try:
        if len(code) == 0:
            return "Nothing in the editor to execute :()"
        with tempfile.NamedTemporaryFile('w', suffix='.py') as f:
            f.write(utils_file)
            f.write(f"\n\n{code}")
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
        return "There's very likely an infinite loop/recursion or a way to do it much quicker. Every solution can be done in under 15 seconds, this has returned after 20."


def submit_answer(year, day, part, token, answer, terminal, instance):
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
    article_text = p_tag.text.strip()

    colour = "green" if "That's the right answer" in article_text else "red"

    terminal.append(f'''<span style="color: {
        colour};">------<br>{article_text}</span>''')

    # Go to part 2 if right so the question can be quickly seen
    if "Answer submitted successfully! That's the right answer." in article_text:
        _, _, part = instance.get_info()
        if part == "1":
            time.sleep(0.5)  # Give it some time to load the page in case

            instance.problem_tabs.setCurrentIndex(1)

    terminal.append("<br>")
    terminal.append(f'<span style="color: black ;"/>')
