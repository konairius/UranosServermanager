from collections import defaultdict

__author__ = 'konsti'


class User(object):
    _latest_id = 0
    _users = dict()
    _permission_map = defaultdict(bool)

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

    def add_permission(self, permission):
        self._permission_map[permission] = True

    def remove_permission(self, permission):
        self._permission_map[permission] = False

    def can_do(self, permission):
        return self._permission_map[permission]