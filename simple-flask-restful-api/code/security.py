from werkzeug.security import safe_str_cmp # for safe string comparison for passwords
from user import User

users = [
    User(1, 'bob', 'asdf')
]

# stores names as the key
username_mapping = {u.username: u for u in users}
userid_mapping = {u.id: u for u in users}

# stores IDs as the key
# line 9 does the same thing but instead with set comprehension
# userid_mapping = { 1: {
#     'id': 1,
#     'username': 'bob',
#     'password': 'asdf'
# }}

# username_mapping['bob']
# userid_mapping[1]
# We do this to make finding our users much quicker instead of iterating through the whole list

def authenticate(username, password):
    """Authentication

    Args:
        username (str): Username
        password (str): Password
    """
    user = username_mapping.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    """Special function for Flask-JWT
    Takes in a payload which is contents of JWT token and we will extract out the userid from payload and once we have that we can retrieve that specific user

    Args:
        payload (str)): JWT Token Contents
    """
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)