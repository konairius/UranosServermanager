from _socket import gethostbyname
from abc import ABCMeta, abstractmethod
from ipaddress import ip_address
from locale import getlocale
import re
from subprocess import Popen, PIPE, DEVNULL
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
    @return:standard unix encoded mac address
    """
    pid = Popen(['arp', '-n', str(ip)], stdout=PIPE)
    s = pid.communicate()[0].decode(getlocale()[1])
    if not 'HWaddress' in s:
        raise KeyError('%(ip)s is not in arp Table' % {'ip': ip})
    mac = re.search(r"(([a-f\d]{1,2}:){5}[a-f\d]{1,2})", s).groups()[0]
    if mac == '':
        raise KeyError('%(ip)s is not in arp Table' % {'ip': ip})
    return mac


def _get_mac_from_arping(ip: ip_address) -> str:
    """
    Much slower than even using arp then ping and arp again,
    but it is a fallback.
    @return:standard unix encoded mac address
    """
    pid = Popen(['arping', '-c1', str(ip)], stdout=PIPE, stderr=DEVNULL)
    s = pid.communicate()[0].decode(getlocale()[1])
    mac = re.search(r"(([A-F\d]{1,2}:){5}[A-F\d]{1,2})", s)
    if mac is None:
        raise KeyError('%(ip)s could not be found' % {'ip': ip})
    mac = mac.groups()[0]
    if mac == '':
        raise KeyError('%(ip)s could not be found' % {'ip': ip})
    return mac


def get_mac_address(ip: ip_address) -> str:
    """
    @return: standard unix encoded mac address
    """
    try:
        return _get_mac_from_arp(ip)
    except KeyError:
        ping(ip, count=1, sync=True)
        try:
            return _get_mac_from_arp(ip)
        except KeyError:
            return _get_mac_from_arping(ip)


class Computer(object):
    def __repr__(self):
        return 'Computer: %(hostname)s(%(ip)s, %(mac)s)' % {'hostname': self.host, 'ip': self.ip, 'mac': self.mac}

    def __init__(self, host: str):
        """
        @param host: Can be either the hostname or the ipaddress as a string
        """
        self.host = host
        self.last_ip = self.ip
        try:
            self.last_mac = get_mac_address(self.ip)
        except KeyError:
            warn('MAC Address could not be determined, you will have to set it manually for some Commands to work',
                 RuntimeWarning)

    @property
    def ip(self) -> ip_address:
        """
        Tries to give you the current ip of the host,
        if it could not be determined, the latest known ip is returned.
        """
        try:
            self.last_ip = ip_address(gethostbyname(self.host))
        except TimeoutError:
            pass
        return self.last_ip

    @property
    def mac(self) -> str:
        try:
            self.last_mac = get_mac_address(self.ip)
        except KeyError:
            pass
        return self.last_mac

    @property
    def status(self) -> 'UP' or 'DOWN':
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

