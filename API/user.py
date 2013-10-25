from Common.models import CommandResult

__author__ = 'konsti'


def add_user(info:str) -> CommandResult:
    """
    Adds a user to the specified system
    @param info: JASON string describing the new user like this:
    {
        "Name": "Manfred Musterman"
        "Password": "Salted Password Hash"
    }
    """