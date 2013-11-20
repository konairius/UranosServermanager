from Common.networking import ping, get_mac_address, Computer

__author__ = 'konsti'

import unittest


class MyTestCase(unittest.TestCase):
    target_hostname = 'fritz.box'
    target_ip = '192.168.178.1'
    target_mac = '9c:c7:a6:7b:61:1a'

    def test_ping(self):
        for r in ping(self.target_ip, count=2):
            self.assertTrue(r is not None)

    def test_get_mac_address(self):
        self.assertEqual(get_mac_address(self.target_ip), self.target_mac)
        self.assertRaises(KeyError, get_mac_address, '127.0.0.1')

    def test_create_computer(self):
        comp = Computer(self.target_hostname)
        self.assertEqual(comp.mac, self.target_mac)
        self.assertEqual(comp.ip, self.target_ip)
        self.assertEqual(comp.host, self.target_hostname)


if __name__ == '__main__':
    unittest.main()
