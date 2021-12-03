import subprocess
from typing import List


def get_input(year: int, day: int) -> List[str]:
    # https://github.com/breakthatbass/eggnog
    process = subprocess.Popen(['nog', '-d', f'{day}', '-y', f'{year}'],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, _ = process.communicate()
    return stdout.decode('utf-8').splitlines()
