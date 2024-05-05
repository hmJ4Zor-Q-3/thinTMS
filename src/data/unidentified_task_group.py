class UnIDTaskGroup:
    def __init__(self, username: str, name: str):
        self.username = username
        self.name = name

    def __eq__(self, other):
        return (isinstance(other, UnIDTaskGroup)
                and (self.username == other.username)
                and (self.name == other.name))
