from datetime import datetime
from app import db

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, email, first_name, last_name, password, is_admin=False, last_login=None):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.is_admin = is_admin
        self.last_login = last_login or datetime.utcnow  # Use the provided last_login or the current time if None

    def __repr__(self):
        return f'<User {self.email}>'
