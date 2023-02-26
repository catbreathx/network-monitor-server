from monitor.database.models import User


class TestUser:
    def test_password_population(self):
        password = "thePassword"

        user = User(password=password)
        assert user.password == password

    def test_password_validation_when_correct(self):
        password = "thePassword"
        user = User(password=password)

        is_correct = user.password == password
        assert is_correct is True

    def test_password_when_incorrect(self):
        user = User(password="abc1234")
        is_correct = user.password == "thePassword"
        assert is_correct is False
