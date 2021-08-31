import requests
from book_managment_app import app
from book_managment_app import db
from flask import render_template, request, session, redirect, url_for, jsonify
from datetime import datetime
from book_managment_app.models.Book import Book
from book_managment_app.forms.BooksApiSearch import SearchInApi
from book_managment_app.forms.AddBooks import AddBooks
from book_managment_app.control import Filters


@app.route("/", methods=["GET", "POST"])
def get_books():
    search = SearchInApi()
    if request.method == "GET":
        return render_template(
            "list_of_books_api.html", search=search, filters=Filters.list_of_filter.keys()
        )
    elif request.method == "POST":
        key = Filters.list_of_filter.get(request.form.get("city"))
        key_word = request.form.get("find")
        books_from_api = _get_data_from_app_api(f'http://localhost:5000/test/api/{key_word}/{key}')
        return render_template(
            "list_of_books_api.html",
            form=books_from_api,
            search=search,
            filters=Filters.list_of_filter.keys(),
        )


@app.route("/add", methods=["GET", "POST"])
def add_books():
    add = AddBooks()
    if request.method == "GET":
        return render_template("add_books_view.html", form=add)
    elif request.method == "POST":
        if add.validate_on_submit():
            add_book_to_library = request.form.to_dict()
            csrf_token = add_book_to_library.pop('csrf_token')
            status = _send_post_request(f'http://localhost:5000/test/add', add_book_to_library)
            print(status)
        return redirect(url_for("show_books"))


@app.route("/show", methods=["GET", "POST"])
def show_books():
    search = SearchInApi()
    list_of_filter = ["author", "title", "language"]
    if request.method == "GET":
        list_of_books = _get_data_from_app_api(f'http://localhost:5000/test')
        return render_template(
            "list_of_books_from_db_view.html",
            form2=list_of_filter,
            form=list_of_books,
            searchfield=search,
        )
    elif request.method == "POST":
        param = request.form.get("choice")
        value = request.form.get("find")
        list_of_books = _get_data_from_app_api(f'http://localhost:5000/test/{param}/{value}')
        return render_template(
                           "list_of_books_from_db_view.html",
                           form2=list_of_filter,
                           form=list_of_books,
                           searchfield=search,
                       )

@app.route("/show/edit", methods=["POST"])
@app.route("/show/edit/<int:book_id>", methods=["POST"])
def edit_book(book_id=None):
    add = AddBooks()
    if request.method == "POST" and book_id is not None:
        session["book_id"] = book_id
        return render_template("add_books_view.html", put_form=add)
    elif request.method == "POST":
        book = db.session.query(Book).filter(Book.id == session["book_id"]).first()
        book.title = request.form.get("title")
        book.author = request.form.get("author")
        book.number_of_pages = request.form.get("number_of_pages")
        book.publication_language = request.form.get("publication_language")
        book.publication_date = datetime.strptime(
            request.form.get("publication_date"), "%Y"
        )
        book.book_cover_link = request.form.get("book_cover_link")
        book.isbn = request.form.get("isbn")
        db.session.commit()
        return redirect(url_for("show_books"))


@app.route("/imports", methods=["POST"])
def import_books():
    import_book_from_api = dict(request.args)
    import_book = Book(**import_book_from_api)
    _add_to_db(import_book)
    return redirect(url_for("show_books"))


def _get_data_from_app_api(url):
    response = requests.get(url)
    return response.json()

def _send_post_request(url,json_data):
    status_information = requests.post(url=url, json=json_data)
    return status_information


def _add_to_db(book_object):
    db.session.add(book_object)
    db.session.commit()
