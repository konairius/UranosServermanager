from Common.models import Command, CommandResult, Time
from Common.networking import Computer
from Common.utils import execute_subprocess

__author__ = 'konsti'


class WOLCommand(Command):
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
