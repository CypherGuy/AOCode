import subprocess
import time
import tempfile


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
