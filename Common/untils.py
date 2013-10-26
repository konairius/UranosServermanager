import random
from shutil import which
import string
import subprocess

__author__ = 'konsti'


def get_random_string(length: int=20) -> str:
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def execute_subprocess(command: list):
    if not which(command[0]) is None:
        subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        raise OSError(
            'The program %(command)s is not installed on your computer.' % {'command': command[0]})
