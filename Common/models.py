from abc import ABCMeta, abstractmethod
from API.models import User
from Common.command import CommandResult, Command
from Common.utils import Time

__author__ = 'konsti'


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