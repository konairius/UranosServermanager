from datetime import datetime
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


def get_subclasses(superclass):
    subclasses = set()
    work = [superclass]
    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if child not in subclasses:
                subclasses.add(child)
                work.append(child)
    return subclasses


class Time(object):
    _timestamp = None

    def __init__(self, timestamp: float):
        self._timestamp = timestamp

    def __str__(self):
        return datetime.fromtimestamp(self._timestamp).isoformat()

    def __repr__(self):
        return str(self._timestamp)

    def __add__(self, other: float):
        self._timestamp += other

    def __sub__(self, other):
        """
        @return the time difference in seconds
        """
        return abs(self._timestamp - other.timestamp)

    def __eq__(self, other):
        return self._timestamp == other.timestamp

    def __gt__(self, other):
        return self._timestamp > other.timestamp

    def __lt__(self, other):
        return self._timestamp < other.timestamp

    def __ge__(self, other):
        return self._timestamp >= other.timestamp

    def __le__(self, other):
        return self._timestamp <= other.timestamp

    @classmethod
    def never(cls):
        return cls(-1)

    @classmethod
    def now(cls):
        return cls(datetime.now().timestamp())

    @property
    def timestamp(self):
        return self._timestamp
