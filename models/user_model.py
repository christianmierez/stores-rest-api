import sqlite3
from db_sql import db_sql

class UserModel(db_sql.Model):
    __tablename__ = 'users'

    id = db_sql.Column(db_sql.Integer, primary_key=True)
    username = db_sql.Column(db_sql.String(80))
    password = db_sql.Column(db_sql.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def json(self):
        return {
            'id': self.id,
            'username': self.username
        }
    
    def save_to_db(self):
        db_sql.session.add(self)
        db_sql.session.commit()

    def delete_from_db(self):
        db_sql.session.delete(self)
        db_sql.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()