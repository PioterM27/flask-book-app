from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,IntegerField


class BooksApiSearch(FlaskForm):
    title = StringField()
    author = StringField()
    publisher = StringField()
    subject = StringField()
    isbn = IntegerField()
    lccn = StringField()
    oclc = StringField()
class SearchInApi(FlaskForm):
    search = StringField()
    submit = SubmitField()
