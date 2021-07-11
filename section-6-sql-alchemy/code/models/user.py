
# third-party imports
import sqlite3
from db import db

class UserModel(db.Model):
    """User Class for user data"""

    # setting this variable to tell SQLAlchemy our table name
    __tablename__ = 'users'

    # setting columns for SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        # creating db connection
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        # running query
        query = f"SELECT * FROM {cls.TABLE_NAME} WHERE username=?"
        result = cursor.execute(query, (username,))
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
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        # running query
        query = f"SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        # close connection
        connection.close()
        return user
