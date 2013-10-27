from _socket import gethostbyname
from abc import ABCMeta, abstractmethod
from ipaddress import ip_address
from locale import getlocale
import re
from subprocess import Popen, PIPE
from warnings import warn
from Common.models import Command, CommandResult

__author__ = 'konsti'


def ping(ip: ip_address, count: int=1, sync: bool=False) -> dict:
    """
    Generator for a dict containing the output of ping in a usable fashion
    """
    pid = Popen(['ping', '-c ' + str(count), str(ip)], stdout=PIPE)
    if sync:
        pid.wait()
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
    if not 'HWaddress' in s:
        raise KeyError('%(ip)s is not in arp Table' % {'ip': ip})
    mac = re.search(r"(([a-f\d]{1,2}:){5}[a-f\d]{1,2})", s).groups()[0]
    if mac == '':
        raise KeyError('%(ip)s is not in arp Table' % {'ip': ip})
    return mac


def get_mac_address(ip: ip_address) -> str:
    """
    @return standard unix encoded mac address
    """
    try:
        return _get_mac_from_arp(ip)
    except KeyError:
        ping(ip, count=1, sync=True)
        return _get_mac_from_arp(ip)


class Computer(object):
    def __repr__(self):
        return 'Computer: %(hostname)s(%(ip)s, %(mac)s)' % {'hostname': self.host, 'ip': self.ip, 'mac': self.mac}

    def __init__(self, host: str):
        """
        @host Can be either the hostname or the ipaddress
        """
        self.host = host
        self.last_ip = self.ip
        try:
            self.mac = get_mac_address(self.ip)
        except KeyError:
            warn('MAC Address could not be determined, you will have to set it manually for some Commands to work',
                 RuntimeWarning)

    @property
    def ip(self):
        """
        Tries to give you the current ip of the host,
        if it could not be determined, the latest known ip is returned.
        """
        try:
            return ip_address(gethostbyname(self.host))
        except TimeoutError:
            return self.last_ip

    @property
    def status(self):
        try:
            ping(self.ip)
            return 'UP'
        except StopIteration:
            return 'DOWN'


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

