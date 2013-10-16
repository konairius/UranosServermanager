from abc import ABCMeta, abstractmethod
from ipaddress import ip_address
from paramiko import SSHClient, PKey
from Common.models import Command, CommandResult

__author__ = 'konsti'


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


class SSHConnection(IPConnection):
    """
    Wrapper for an SSH connection,
    uses paramiko, a native python ssh library
    """

    _username = None
    _private_key = None
    _host_key = None

    def __init__(self, ip: ip_address, port: int=22, username: str='', private_key: str='', host_key: str=''):
        super().__init__(ip, port)
        self._username = username
        self._private_key = private_key
        self._host_key = host_key

    def _get_open_ssh_client(self) -> SSHClient:
        client = SSHClient()
        client.get_host_keys().add(self._ip.compressed, 'ssh-rsa', PKey(data=self._host_key))

    def execute(self, command: Command) -> CommandResult:
        pass


