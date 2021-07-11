# third-party imports
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

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        """Find user by username

        Args:
            username (string): username

        Returns:
            UserModel: UserModel object
        """
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        """Find user by id

        Args:
            id (string): id of user

        Returns:
            UserModel: UserModel object
        """
        return cls.query.filter_by(id=_id).first()