import locale
import subprocess
from Common.exceptions import ExecutableNotFoundError

__author__ = 'konsti'

"""
This is a wrapper for Openssh-Client,
it is used to provide access to ssh
in an Object-Oriented style.
"""


def find_ssh_executable(ssh_name: str='ssh') -> str:
    call = subprocess.Popen(['which', ssh_name], stdout=subprocess.PIPE)
    call.wait()
    if call.returncode == 0:
        return call.stdout.readline().decode(locale.getlocale()[1]).strip()
    else:
        raise ExecutableNotFoundError(
            'The ssh executable was not found. The Return code of "which" was %(return_code)i' % {
                'return_code': call.returncode})
