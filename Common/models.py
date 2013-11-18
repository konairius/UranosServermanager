from abc import ABCMeta, abstractmethod
from datetime import datetime

__author__ = 'konsti'


class User(object):
    _latest_id = 0
    _users = dict()

    #noinspection PyAttributeOutsideInit
    @classmethod
    def reset_users(cls):
        cls._latest_id = 0
        cls._users = dict()

    @classmethod
    def get_next_id(cls) -> int:
        cls._latest_id += 1
        return cls._latest_id

    @classmethod
    def add_user(cls, user):
        if user.id in cls._users.keys():
            raise KeyError(
                'The UserId %(id)i is already given to %(current)s' % {'id': user.id, 'current': cls._users[user.id]})
        cls._users[user.id] = user

    def __init__(self, name: str):
        self._name = name
        self._id = self.get_next_id()
        self.add_user(self)

    def __str__(self):
        return self._name

    def __repr__(self):
        return str(self._id)

    @property
    def id(self):
        return self._id


class Time(object):
    _timestamp = None

    def __init__(self, timestamp: float):
        self._timestamp = timestamp

    def __str__(self):
        return datetime.fromtimestamp(self._timestamp).isoformat()

    def __repr__(self):
        return str(self._timestamp)

    def __add__(self, other: float):
        self._timestamp += other

    def __sub__(self, other):
        """
        @return the time difference in seconds
        """
        return abs(self._timestamp - other.timestamp)

    def __eq__(self, other):
        return self._timestamp == other.timestamp

    def __gt__(self, other):
        return self._timestamp > other.timestamp

    def __lt__(self, other):
        return self._timestamp < other.timestamp

    def __ge__(self, other):
        return self._timestamp >= other.timestamp

    def __le__(self, other):
        return self._timestamp <= other.timestamp

    @classmethod
    def never(cls):
        return cls(-1)

    @classmethod
    def now(cls):
        return cls(datetime.now().timestamp())

    @property
    def timestamp(self):
        return self._timestamp


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


class Job(metaclass=ABCMeta):
    """
    This is the baseclass for all
    Jobs, it specifies some interfaces
    so business logic can be implemented
    in the according Subclass
    """

    def __init__(self, creator: User, command: Command):
        self._creation_time = Time.now()
        self._creator = creator
        self._command = command

    @property
    @abstractmethod
    def next_execution(self) -> Time:
        return None

    def __call__(self, *args, **kwargs) -> CommandResult:
        return self._command(args, kwargs)


class OnetimeJob(Job):
    _execution_time = None

    @property
    def next_execution(self) -> Time:
        if self._execution_time < Time.now():
            return Time.never()
        return self._execution_time


class RecurringJob(Job):
    _first_execution = None
    _latest_execution = None
    _last_execution = None
    _interval = None

    @property
    def next_execution(self) -> Time:
        time = self._latest_execution
        while time < Time.now():
            if time > self._last_execution:
                return Time.never()
            time += self._interval
        return time


class Serializable(metaclass=ABCMeta):
    """
    Baseclass for a object that can be saved to the database
    """

    @property
    def base_name(self) -> str:
        """
        @return: the basename of the class, the collection will be called like this
        """
        return self.__name__

    @property
    def serial(self) -> dict:
        """
        By default just the __dict__ object, but it can be any dict that is used by from_serial()
        to recreate the object.
        @return: the dict used to recreate the object from serialized data
        """
        return self.__dict__

    @classmethod
    @abstractmethod
    def from_serial(cls, serial: dict):
        """
        @param serial: the dict create by the "serial" property
        @return: an instance of the object
        """
        pass