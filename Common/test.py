import random
import string
from time import sleep
from Common.exceptions import InvalidCommandStateError, ExecutableNotFoundError, InvalidCommandNameError
from Common.models import User, Time, CommandResult
from Common.networking import SSHKey
from Common.untils import execute_subprocess
from UptimeManager.models import WOLCommand

__author__ = 'konsti'

import unittest


def string_generator(size=6, chars=string.ascii_letters + string.digits):
    #noinspection PyUnusedLocal
    return ''.join(random.choice(chars) for x in range(size))


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
        self.assertRaises(InvalidCommandStateError, result.set_state, 'invalid_state')


class TestClassWOLCommand(unittest.TestCase):
    def test_create(self):
        name = 'wake'
        cmd = WOLCommand(name)
        self.assertEqual(cmd.name, name)
        self.assertRaises(InvalidCommandNameError, WOLCommand, name)


class TestGlobalUtilFunctions(unittest.TestCase):
    @staticmethod
    def test_execute_existing_subprocess():
        execute_subprocess(['ls', '-l'])

    def test_execute_nonexistent_subprocess(self):
        self.assertRaises(ExecutableNotFoundError, execute_subprocess, ['not_existing_command', '-ds'])


class TestClassSSHKey(unittest.TestCase):
    public_key = """ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCxG8T7
oh8wrYfFWT+ztvDJgPRp6g2Bi6ejp3rGt7bsGTxVMkkb2IPio84bfCg0P2PW
qfWeNlzNpnKFGtbp3tnl6QvG7HQzVRwYOAglXV1VEpXJEJ8VjJwOEvI6qQlI
FanMgz8JXWBQu/0IpssfnZEwlSJWpZsv4g5EE7ZlfiocMfXAYRip15JlbEWk
4a6AnQ3G4uVMt6HlyL+D0iD740LUCYKV9Xabz3XIFrU8v9JqAdwVfWonz54/
DZnjrHOYMS0ixYTN4PBdQ9xxKHUek/t9M2AswIF+9FwupiwInoV/oOMEV6wx
ym+/XA6Waz4X1+ADe+cg0q/1UpDzCN3EUb9B konsti@konsti-laptop"""

    private_key = """-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEAsRvE+6IfMK2HxVk/s7bwyYD0aeoNgYuno6d6xre27Bk8VTJJ
G9iD4qPOG3woND9j1qn1njZczaZyhRrW6d7Z5ekLxux0M1UcGDgIJV1dVRKVyRCf
FYycDhLyOqkJSBWpzIM/CV1gULv9CKbLH52RMJUiVqWbL+IORBO2ZX4qHDH1wGEY
qdeSZWxFpOGugJ0NxuLlTLeh5ci/g9Ig++NC1AmClfV2m891yBa1PL/SagHcFX1q
J8+ePw2Z46xzmDEtIsWEzeDwXUPccSh1HpP7fTNgLMCBfvRcLqYsCJ6Ff6DjBFes
Mcpvv1wOlms+F9fgA3vnINKv9VKQ8wjdxFG/QQIDAQABAoIBAQCYCGCGKdtga/Y6
wKxgV1BHib1GFjbV185mO+S3JQmPjvItqGb90lUUfsz05xWUFD5eDbPcxonPt2xj
OnD2fejK5czITD5LumnNmHvVp1nxJ20RFoWZeASWSElLdcOT75S9DIVWQqPlahqC
DLwdPaNe8wZxHuQirIjWg511bmIzpHhQ1LfffQN4MHR5GqCytqLngu8p9OGVsj6y
qGEw+EyDwBBKDEIvPQvvjsgOkbPZyQH+KraCr4cp8hRTmxLL2/+Ca5z5zOtIzBUz
splwvh2BoqzHpfGcYWUcCXv7W15/lZlzprdkgJfkOOQSOdsqxhjI5dGlzIDWIrZg
8YO1vtYBAoGBAOmLjikke2bgkRNF9er8qnPl3AHlkX3NEaqAZHWA9YjoalJHl+ag
KZ9AfRVBHAx3pacmZLdEi6Waus+sn3T89rOXyqOHsN7mJh7pnoVhs2Oe3SS4nW+m
74z8iqTOdpQT5rD0ECsYDBuufzZNc10YklE2L6jVu6R+SQaSHwvijdzRAoGBAMIj
FzUkYGNyovM0CEl07yT8a+MnNKZkU5IcUtmf9m3Yc+CQMvgSleybFPi4T+pVpbvz
MqIivDahdcXLHdIB8BiEGDcLQn4fYIOMZk0ZHgOm5KaY8Bb1AoAC2lHrUVEH48ON
72ARV+edkY0ygeyuDJ2F0P7/g+XpYiUT5Id8NJdxAoGAGiODcrlhkl8Z/aU74+QJ
k9UrLY8rHIBiNMoP9FLNqFgS5kibCLXuUqOeHE3gPMj7YlzasuRaGNvbgrjYU/io
B+u6Q1lBg4EQzS7qjhUkRccXCzAads+hSg9N2So+fU5I6I84bApR+JssI8DBY68H
WU2OQgBB8yQrOjAKh4MAy7ECgYEAnbIJYPZ6gW2WJb3HWXvt4fpU3MB1CRAHvnDZ
b8N7VkDz557aeB4IwJg8kciNycjmhmSHZaKXhjzjQNa8E2HVmOR8EwJHcdGlAVZj
pw7XDZpcs2MZ61v8OuWWV+KxPAQPpELABiYwZIjeuXYkiY/b2XzghrIhfvlz6rBc
+x0OT1ECgYEA4/W+v/t3WOA0dU1xNk1dYcjgObtVmyCw5EE6qXnO2zPUf/WyFrUS
n/ipXKcC4UmbVUEeq+FcxCtTeiWx9lo9S7RUTjl1esXJNTAchl1hA1UtGa77Qg3y
/ib3Oglr5sNzPuojcLlSR0GeKo6JxcTsd3tcfDPk8GYzvYkfq60ApwE=
-----END RSA PRIVATE KEY-----"""

    def test_create(self):
        key = SSHKey(public=self.public_key, private=self.private_key)
        self.assertEqual(key.public, self.public_key)
        self.assertEqual(key.private, self.private_key)

    def test_file(self):
        key = SSHKey(public=self.public_key, private=self.private_key)
        print(key.private_file)


if __name__ == '__main__':
    unittest.main()
