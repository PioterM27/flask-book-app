from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField, DateField, validators
from wtforms.validators import (
    InputRequired,
    Length,
    AnyOf,
    DataRequired,
    ValidationError,
)


class AddBooks(FlaskForm):
    title = StringField(
        label="Title",
        validators=[
            DataRequired(),
            Length(min=2, max=200, message="Title should least %(min)d character"),
        ],
    )
    author = StringField("Author")
    publication_date = DateField(
        "Publication Date",
        validators=[DataRequired(message="Date should be in format %Y")],
        format="%Y-%m-%d",
    )
    number_of_pages = StringField("Number of Pages", validators=[DataRequired()])
    isbn = StringField(
        "ISBN number",
        validators=[DataRequired(), Length(13, message="ISBN should 13 characters")],
    )
    book_cover_link = StringField("Link")
    publication_language = StringField(
        "Publication language",
        validators=[DataRequired(), Length(2, message="language should 2 characters")],
    )
