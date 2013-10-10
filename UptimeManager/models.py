from Common.models import Command, Computer
from Common.untils import execute_subprocess

__author__ = 'konsti'


class WOLCommand(Command):

    def __call__(self, target: Computer):
        execute_subprocess(['etherwake', target.macaddress])
