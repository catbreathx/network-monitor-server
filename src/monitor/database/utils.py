import bcrypt


class PasswordHash(object):
    def __init__(self, password_hash: str):
        password_has_bytes = password_hash.encode("utf-8")
        assert len(password_has_bytes) == 60, "bcrypt hash should be 60 chars."
        assert password_has_bytes.count(b"$"), 'bcrypt hash should have 3x "$".'
        self.hash = password_has_bytes
        self.rounds = int(self.hash.split(b"$")[2])

    def __eq__(self, password):
        result = False

        if isinstance(password, str):
            candidate = password.encode("utf-8")
            result = bcrypt.checkpw(candidate, self.hash)

        return result

    def __repr__(self):
        """Simple object representation."""
        return "<{}>".format(type(self).__name__)

    @classmethod
    def new(cls, password, rounds):
        if isinstance(password, str):
            password = password.encode("utf-8")

        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt(rounds))

        instance = cls(hashed_password.decode("utf-8"))
        return instance
