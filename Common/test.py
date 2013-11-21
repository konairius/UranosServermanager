import random
import string
from time import sleep
from Common.models import User, Time, CommandResult
from Common.utils import execute_subprocess
from UptimeManager.models import WOLCommand

__author__ = 'konsti'

import unittest


def string_generator(size=6, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class TestClassUser(unittest.TestCase):
    def test_create(self):
        User.reset_users()
        name = 'Konstantin Renner'
        user = User(name)
        self.assertEqual(str(user), name)
        self.assertEqual(user.id, User(name).id - 1)

    def test_mass_create(self):
        User.reset_users()
        size = 10000
        users = dict()
        for i in range(size):
            users[i] = User(string_generator())
        for i in range(len(users)):
            self.assertEqual(i, users[i].id - 1)


class TestClassTime(unittest.TestCase):
    def test_create(self):
        time = Time.now()
        sleep(1)
        self.assertLess(time, Time.now())


class TestClassCommandResult(unittest.TestCase):
    valid_states = ['unknown', 'successful', 'failed', 'running']

    def test_create(self):
        result = CommandResult()
        for state in self.valid_states:
            result.set_state(state)
        self.assertRaises(RuntimeError, result.set_state, 'invalid_state')


class TestClassWOLCommand(unittest.TestCase):
    def test_create(self):
        name = 'wake'
        cmd = WOLCommand(name)
        self.assertEqual(cmd.name, name)
        self.assertRaises(KeyError, WOLCommand, name)


class TestGlobalUtilFunctions(unittest.TestCase):
    @staticmethod
    def test_execute_existing_subprocess():
        execute_subprocess(['ls', '-l'])

    def test_execute_nonexistent_subprocess(self):
        self.assertRaises(OSError, execute_subprocess, ['not_existing_command', '-ds'])


if __name__ == '__main__':
    unittest.main()
