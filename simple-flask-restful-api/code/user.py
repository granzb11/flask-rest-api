import sqlite3
class User:
    """User Class for user data"""

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        # creating db connection
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # running query
        query = f"SELECT * FROM users WHERE username = {username}"
        result = cursor.execute(query)
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        # close connection
        connection.close()
        return user

    @classmethod
    def find_by_id(cls, id):
        # creating db connection
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # running query
        query = f"SELECT * FROM users WHERE id = {id}"
        result = cursor.execute(query)
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        # close connection
        connection.close()
        return user