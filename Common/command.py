from abc import ABCMeta, abstractmethod
from locale import getlocale
from subprocess import Popen, PIPE
from Common.networking import Computer
from Common.utils import get_subclasses, Time, execute_subprocess

__author__ = 'konsti'


class CommandResult(object):
    _state = str()

    def __init__(self):
        self._state = 'unknown'
        self._message = 'not set'

    def __str__(self):
        return 'Result: %(state)s\nMessage: %(message)s' % {'state': self._state, 'message': self._message}


    @property
    def message(self):
        return self._message

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state: ['unknown', 'successful', 'failed', 'running']):
        if not new_state in ['unknown', 'successful', 'failed', 'running']:
            raise RuntimeError('%(state)s is not a valid State.' % {'state': new_state})
        self._state = new_state

    @message.setter
    def message(self, new_message):
        self._message = new_message


class Command(metaclass=ABCMeta):
    """
    Baseclass for all commands
    """
    _commands = dict()

    @classmethod
    @abstractmethod
    def from_json(cls, json: dict):
        """
        @param json: a command description like this:
        {
            "type": "CommandType",
            "args": {
                "arg_name": "arg"
                }
        }
        @return: an instance of the command described in json
        """
        subclasses = dict((item.__name__, item) for item in get_subclasses(cls))

        try:
            return subclasses[json['type']].from_json(json['args'])
        except KeyError:
            raise SyntaxError('%(type)s is not a Valid command Type' % {'type': json['type']})

    @abstractmethod
    def __call__(self, *args, **kwargs) -> CommandResult:
        pass


class ExecuteCommand(Command):
    """
    This Command type executes an executable.
    """

    @classmethod
    def from_json(cls, json: dict):
        """
        @param json: a command description like this:
        {
        "executable": "/bin/ls",
        "args":
            [
                "-l",
                "-a"
            ]
        }
        @return: an instance of the command described in json
        """
        return cls(json['executable'], json['args'])

    def __init__(self, executable: str, args: list):
        self.executable = executable
        self.args = args

    def __call__(self, additional_args=list(), sync=False) -> CommandResult:
        result = CommandResult()
        args = self.args
        args.append(additional_args)
        args.insert(0, self.executable)
        pid = Popen(args, stdout=PIPE)
        result.state = 'running'
        result.message = 'Execution started at %(time)s\nStdout:\n' % {'time': Time.now()}
        if sync:
            pid.wait()
            result.message += pid.stdout.read().decode(getlocale()[1])
        return result


class WOLCommand(Command):
    @classmethod
    def from_json(cls, json: dict):
        """\
        @param json: as WOLCommand has only static members this can be empty, it is not parsed:
        {
        }
        @return: an instance of the command described in json
        """
        return WOLCommand

    def __call__(self, target: Computer, sync=False, timeout=100) -> CommandResult:
        execute_subprocess(['etherwake', target.mac])
        result = CommandResult()
        start = Time.now()
        if sync:
            result.state = 'failed'
            while not target.status == 'UP' and Time.now() - start < timeout:
                pass

        if target.status == 'UP':
            result.state = 'successful'
        result.message = 'Ping returned after %(time)s seconds' % {'time': str(Time.now() - start)}
        return result
