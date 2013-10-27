from abc import ABCMeta, abstractmethod
from ipaddress import ip_address
from locale import getlocale
import re
from subprocess import Popen, PIPE
from Common.models import Command, CommandResult

__author__ = 'konsti'


def ping(ip: ip_address, count: int=1) -> float:
    """
    Generator for a dict containing the output of ping in a usable fashion
    """
    pid = Popen(['ping', '-c ' + str(count), str(ip)], stdout=PIPE)
    while True:
        next_line = pid.stdout.readline().decode(getlocale()[1])
        if pid.poll() is not None and next_line == '':
            break
        if 'bytes from' in next_line:
            result_string = next_line.split(':')[1].strip()[:-3]
            yield dict(item.split('=') for item in result_string.split(' '))


def _get_mac_from_arp(ip: ip_address) -> str:
    """
    @return standard unix encoded mac address
    """
    pid = Popen(['arp', '-n', str(ip)], stdout=PIPE)
    s = pid.communicate()[0].decode(getlocale()[1])
    mac = re.search(r"(([a-f\d]{1,2}:){5}[a-f\d]{1,2})", s).groups()[0]
    if mac == '':
        raise KeyError('{ip}s is not in arp Table' % {'ip': ip})
    return mac


def get_mac_address(ip: ip_address) -> str:
    """
    @return standard unix encoded mac address
    """
    try:
        return _get_mac_from_arp(ip)
    except KeyError:
        ping(ip)
        return _get_mac_from_arp(ip)


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

