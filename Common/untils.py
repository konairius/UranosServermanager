import subprocess
from Common.exceptions import ExecutableNotFoundError

__author__ = 'konsti'


def execute_subprocess(command: list):
    if 0 == subprocess.call(['which', command[0]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL):
        subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        raise ExecutableNotFoundError(
            'The program %(command)s is not installed on your computer.' % {'command': command[0]})