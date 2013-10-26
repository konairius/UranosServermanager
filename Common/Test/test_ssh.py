import unittest
from Common.ssh import find_ssh_executable

__author__ = 'konsti'


class TestBasicAutoconfig(unittest.TestCase):
    executable_path = '/usr/bin/ssh'

    def test_find_ssh_executable(self):
        path = find_ssh_executable()
        self.assertEqual(path, self.executable_path)


if __name__ == '__main__':
    unittest.main()
