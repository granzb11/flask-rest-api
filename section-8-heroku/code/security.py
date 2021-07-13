from werkzeug.security import safe_str_cmp  # for safe string comparison for passwords
from models.user import UserModel

def authenticate(username, password):
    """Authentication

    Args:
        username (str): Username
        password (str): Password
    """
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    """Special function for Flask-JWT
    Takes in a payload which is contents of JWT token and we will extract out the userid from payload and once we have that we can retrieve that specific user

    Args:
        payload (str)): JWT Token Contents
    """
    user_id = payload["identity"]
    return UserModel.find_by_id(user_id)
