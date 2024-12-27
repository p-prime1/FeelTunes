from models import User

def test_valid_user(valid_user):
    assert valid_user.username == "test"
    assert valid_user.email == "test@gmail.com"
    assert valid_user.email is not "test1234"


def test_database_session(valid_user, db_session):
    db_session.add(valid_user)
    db_session.commit()
