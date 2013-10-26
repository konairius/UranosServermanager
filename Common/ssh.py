from ipaddress import ip_address
from shutil import which
import tempfile
from Common.models import Command, CommandResult
from Common.networking import IPConnection

__author__ = 'konsti'

"""
This is a wrapper for Openssh-Client,
it is used to provide access to ssh
in an Object-Oriented style.
"""


class SSHKey(object):
    """
    Container class for an ssh key
    """

    def __init__(self, public: str='', private: str='', key_type: str='ssh-rsa'):
        self._public = public
        self._private = private
        self._key_type = key_type

    @property
    def public(self) -> str:
        return self._public

    @property
    def private(self) -> str:
        return self._private

    @property
    def key_type(self) -> str:
        return self._key_type

    @property
    def private_file(self) -> tempfile:
        file = tempfile.NamedTemporaryFile('w+t')
        file.write(self.private)
        file.seek(0)
        return file


def find_ssh_executable(ssh_name: str='ssh') -> str:
    path = which(ssh_name)
    if path is None:
        raise OSError('The ssh executable was not found.')
    return path


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

    def execute(self, command: Command) -> CommandResult:
        pass
