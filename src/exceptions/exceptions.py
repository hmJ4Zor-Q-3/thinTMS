class UsernameError(Exception):
    """
    Error semantically denoting an issue occurred with a username. Doesn't currently exist, does currently exist, etc.
    """
    pass


class PasswordError(Exception):
    """
    Error semantically denoting an issue occurred with a password. Hash didn't match, not secure enough, etc.
    """
    pass


class AuthTokenError(Exception):
    """
    Error semantically denoting an issue occurred with a given authentication token. Didn't match record, expired, etc.
    """
    pass
