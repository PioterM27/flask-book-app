from book_managment_app import db
from sqlalchemy.orm import validates
from datetime import datetime


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    publication_date = db.Column(db.DateTime, default=datetime.utcnow)
    isbn = db.Column(db.BigInteger, nullable=False, unique=True)
    number_of_pages = db.Column(db.Integer, nullable=False)
    book_cover_link = db.Column(db.String(3000), nullable=False)
    publication_language = db.Column(db.String(20), nullable=False)

    @validates('publication_date')
    def convert_str_to_date_type(self,key,publication_date):
        if type(publication_date) is str:
            publication_date = datetime.strptime(publication_date, "%Y-%m-%d")
            return publication_date





    def return_json(self):
        book_to_json = {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "publication_date": self.publication_date.year,
            "isbn": self.isbn,
            "number_of_pages": self.number_of_pages,
            "book_cover_link": self.book_cover_link,
            "publication_language": self.publication_language,
        }
        return book_to_json
