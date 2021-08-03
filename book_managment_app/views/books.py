from book_managment_app import app
from book_managment_app import db
from flask import render_template, request, session, redirect, url_for
from datetime import datetime
from book_managment_app.models.Book import Book
from book_managment_app.control.GetBookList import GetBookList
from book_managment_app.forms.BooksApiSearch import SearchInApi
from book_managment_app.forms.AddBooks import AddBooks
from flask_bootstrap import Bootstrap


@app.route("/", methods=["GET", "POST"])
def get_books():
    list_of_filter = {
        "author": "inauthor",
        "title": "intitle",
        "isbn": "isbn",
        "subject": "subject",
        "publisher": "inpublisher",
    }
    search = SearchInApi()
    if request.method == "GET":
        return render_template(
            "list_of_books_api.html", search=search, filters=list_of_filter.keys()
        )
    elif request.method == "POST":
        key = list_of_filter.get(request.form.get("city"))
        key_word = request.form.get("find")
        test = GetBookList(key_word, key)
        results2 = test.get_response()
        return render_template(
            "list_of_books_api.html",
            form=results2,
            search=search,
            filters=list_of_filter.keys(),
        )


@app.route("/add", methods=["GET", "POST", "PUT"])
def add_books():
    print("jestem tutaj1")
    add = AddBooks()
    if request.method == "GET":
        return render_template("add_books_view.html", form=add)
    elif request.method == "POST":
        if add.validate_on_submit():
            new__db_record = Book()
            new__db_record.title = request.form.get("title")
            new__db_record.author = request.form.get("author")
            new__db_record.publication_date = datetime.strptime(
                request.form.get("publication_date"), "%Y"
            )
            new__db_record.isbn = request.form.get("isbn")
            new__db_record.number_of_pages = request.form.get("number_of_pages")
            new__db_record.book_cover_link = request.form.get("book_cover_link")
            new__db_record.publication_language = request.form.get(
                "publication_language"
            )
            db.session.add(new__db_record)
            db.session.commit()
        return render_template("add_books_view.html", form=add)


@app.route("/show", methods=["GET", "POST"])
def show_books():
    search = SearchInApi()
    list_of_filter = ["author", "title", "language"]
    books = Book.query
    list_of_books = []
    if request.method == "GET":
        for book in books:
            list_of_books.append(book.return_json())
        return render_template(
            "list_of_books_from_db_view.html",
            form2=list_of_filter,
            form=list_of_books,
            searchfield=search,
        )
    elif request.method == "POST":
        param = request.form.get("choice")
        value = request.form.get("find")
        if param == "title":
            filter_books = Book.query.filter(Book.title == value).all()
            if not filter_books:
                return render_template(
                    "list_of_books_from_db_view.html",
                    form2=list_of_filter,
                    form=list_of_books,
                    searchfield=search,
                )
        elif param == "author":
            filter_books = Book.query.filter(Book.author == value).all()
            if not filter_books:
                return render_template(
                    "list_of_books_from_db_view.html",
                    form2=list_of_filter,
                    form=list_of_books,
                    searchfield=search,
                )
        elif param == "language":
            filter_books = Book.query.filter(Book.publication_language == value).all()
            if not filter_books:
                return render_template(
                    "list_of_books_from_db_view.html",
                    form2=list_of_filter,
                    form=list_of_books,
                    searchfield=search,
                )
        for book in filter_books:
            list_of_books.append(book.return_json())
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
    print(request.args.get("title"))
    print(request.args)
    print(request.args.get("pubdate"))
    print(request.json)
    import_book = Book()
    import_book.title = request.args.get("title")
    import_book.author = request.args.get("author")
    import_book.publication_date = datetime.strptime(
        request.args.get("pubdate"), "%Y-%m-%d"
    )
    import_book.isbn = request.args.get("isbn")
    import_book.number_of_pages = request.args.get("page_nbr")
    import_book.book_cover_link = request.args.get("cover")
    import_book.publication_language = request.args.get("language")
    db.session.add(import_book)
    db.session.commit()
    return redirect(url_for("show_books"))
