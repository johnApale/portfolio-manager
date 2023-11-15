from app import db  # Import the SQLAlchemy instance from your app package
from sqlalchemy import ARRAY, DateTime

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    date_created = db.Column(DateTime, nullable=False)
    description = db.Column(db.Text, nullable=False)
    photos = db.Column(ARRAY(db.String(255)))

    def __init__(self, name, date_created, description, photos=None):
        self.name = name
        self.date_created = date_created
        self.description = description
        self.photos = photos or []

    def __repr__(self):
        return f'<Project {self.name}>'
