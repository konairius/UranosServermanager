from shutil import which
from Common.exceptions import ExecutableNotFoundError

__author__ = 'konsti'

"""
This is a wrapper for Openssh-Client,
it is used to provide access to ssh
in an Object-Oriented style.
"""


def find_ssh_executable(ssh_name: str='ssh') -> str:
    path = which(ssh_name)
    if path is None:
        raise ExecutableNotFoundError('The ssh executable was not found.')
    return path

