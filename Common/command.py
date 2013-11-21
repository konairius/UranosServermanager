from abc import ABCMeta, abstractmethod

__author__ = 'konsti'


class Command(metaclass=ABCMeta):
    """
    Baseclass for all commands
    """
    _commands = dict()

    def __init__(self, name: str):
        """
        This constructor must be called by all Child classes,
        it is used to keep track of the known commands and
        avoid naming issues (names have to be unique).
        """
        self._name = name
        self.add_command(self)

    @classmethod
    def add_command(cls, command):
        # It really should be Command._commands not cls._commands
        # because commands a cached globally.
        if command.name in Command._commands.keys():
            raise KeyError('The Command %(name)s already exists' % {'name': command.name})
        Command._commands[command.name] = command

    @abstractmethod
    def __call__(self, *args, **kwargs) -> CommandResult:
        pass

    @property
    def name(self):
        return self._name


class ExecutableCommand(Command):
    """
    This Command type executes an executable.
    """

    def __init__(self, name: str, exe: str, arg: list):
        self.exe = exe
        self.arg = arg
        super().__init__(name)

    def __call__(self, computer, additional_args=list(), sync=False) -> CommandResult:
        pass


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
