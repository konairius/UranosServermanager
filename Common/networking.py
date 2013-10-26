from abc import ABCMeta, abstractmethod
from netaddr import EUI, IPAddress
from Common.models import Command, CommandResult

__author__ = 'konsti'


def get_mac_address(ip: IPAddress) -> EUI:
    pass


class Computer(object):
    def __init__(self, host):
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

