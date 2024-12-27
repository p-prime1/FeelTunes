from models import User

def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password
    """
    user = User('patric@gmail.com', 'FlaskIsAwesome')
    assert user.email == 'patric@gmail.com'
    assert user.hashed_password != 'FlaskIsAwesome'
