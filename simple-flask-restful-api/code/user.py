import sqlite3
from flask_restful import Resource, reqparse

class User:
    """User Class for user data"""

    TABLE_NAME = "users"

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

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", type=str, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "password", type=str, required=True, help="This field cannot be left blank!"
    )

    def post(self):
        data = UserRegister.parser.parse_args()
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        # execute query
        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data["username"], data["password"]))

        # commit and close connection
        connection.commit()
        connection.close()

        return {"message": "User created successfully"}, 201