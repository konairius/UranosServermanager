from abc import ABCMeta, abstractmethod
from ipaddress import ip_address
from paramiko import SSHClient, PKey
from Common.models import Command, CommandResult

__author__ = 'konsti'


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


class SSHKey(object):
    """
    Container class for an ssh key
    """

    def __init__(self, public, private: str='', key_type: str='ssh-rsa'):
        self._public = public
        self._private = private
        self._key_type = key_type

    @property
    def public(self):
        return self.public

    @property
    def private(self):
        return self.private

    @property
    def key_type(self):
        return self._key_type


class SSHConnection(IPConnection):
    """
    Wrapper for an SSH connection,
    uses paramiko, a native python ssh library
    """

    _username = None
    _user_key = None
    _host_key = None

    def __init__(self, username: str, user_key: SSHKey,
                 host_key: SSHKey, ip: ip_address, port: int=22):
        """
        @param username: username on the remote machine
        @param user_key: private key must be set in this case
        @param host_key: private key can (and should) be empty
        """
        super().__init__(ip, port)
        self._username = username
        self._user_key = user_key
        self._host_key = host_key

    def _get_open_ssh_client(self) -> SSHClient:
        client = SSHClient()
        client.get_host_keys().add(self._ip.compressed, self._host_key.key_type, PKey(data=self._host_key.public))
        return client

    def execute(self, command: Command) -> CommandResult:
        pass


