from book_managment_app import db
from datetime import datetime


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    publication_date = db.Column(db.DateTime, default=datetime.utcnow)
    isbn = db.Column(db.BigInteger, nullable=False, unique=True)
    number_of_pages = db.Column(db.Integer, nullable=False)
    book_cover_link = db.Column(db.String(50), nullable=False)
    publication_language = db.Column(db.String(20), nullable=False)
