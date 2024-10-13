from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    overview = db.Column(db.Text, nullable=False)
    release_date = db.Column(db.Date, nullable=True)
    poster_path = db.Column(db.String(200), nullable=True)