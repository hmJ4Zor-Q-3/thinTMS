from typing import NamedTuple


class User(NamedTuple):
    username: str
    password: str
    auth_token: str

