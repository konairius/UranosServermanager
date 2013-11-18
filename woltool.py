from argparse import ArgumentParser
import shelve
from Common.networking import Computer
from UptimeManager.models import WOLCommand

__author__ = 'konsti'

computers = dict()


def main():
    parser = ArgumentParser(description='Simple WOL Tool')
    parser.add_argument('command', choices=['wake', 'create', 'list', 'status'])
    parser.add_argument('-n', '--name', help='The Hostname of the machine', nargs='+')

    args = parser.parse_args()

    load()

    if args.command == 'create':
        for name in args.name:
            computers[name] = Computer(name)
    elif args.command == 'wake':
        cmd = WOLCommand('wol')
        for name in args.name:
            print(cmd(computers[name], sync=True))

    elif args.command == 'list':
        for name in computers:
            print(name)

    elif args.command == 'status':
        for name in computers:
            print(name, computers[name].status, sep=': ')

    save()


def load():
    cache = shelve.open('cache')
    for key in cache:
        computers[key] = cache[key]
    cache.close()


def save():
    cache = shelve.open('cache')
    for computer in computers.values():
        cache[computer.host] = computer
    cache.close()


if __name__ == '__main__':
    main()