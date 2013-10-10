from abc import ABCMeta, abstractmethod
import logging

__author__ = 'konsti'

logger = logging.getLogger(__name__)


class UranosError(Exception, metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, message: str):
        logger.exception(message)

    @staticmethod
    def debug(message: str):
        logger.debug(message)

    @staticmethod
    def info(message: str):
        logger.info(message)

    @staticmethod
    def warning(message: str):
        logger.warning(message)

    @staticmethod
    def error(message: str):
        logger.error(message)


class InvalidUserIdError(UranosError):
    def __init__(self, message: str):
        self.error(message)


class InvalidCommandStateError(UranosError):
    def __init__(self, message: str):
        self.error(message)


class InvalidCommandNameError(UranosError):
    def __init__(self, message: str):
        self.error(message)


class ExecutableNotFoundError(UranosError):
    def __init__(self, message: str):
        self.warning(message)