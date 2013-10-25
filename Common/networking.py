from abc import ABCMeta, abstractmethod
from ipaddress import ip_address
from Common.models import Command, CommandResult

__author__ = 'konsti'


class Computer(object):
    def __init__(self, hostname: str, ip: str='', network: str=''):
        pass


class Connection(object, metaclass=ABCMeta):
    """
    Baseclass for all connection wrappers,
    must be implemented by all connections
    """

    @abstractmethod
    def execute(self, command: Command) -> CommandResult:
        pass


class IPConnection(object, metaclass=ABCMeta):
    """
    This a wrapper to enable abstract network communication,
    specific communication methods MUST inherit from it
    """
    _ip = None
    _service_port = None

    def __init__(self, ip: ip_address, port: int):
        self._ip = ip
        self._service_port = port

    @abstractmethod
    def execute(self, command: Command) -> CommandResult:
        pass

