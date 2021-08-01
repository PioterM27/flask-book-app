from book_managment import app
from flask import render_template, request
from book_managment_app.control.GetBookList import GetBookList
from book_managment_app.forms.BooksApiSearch import SearchInApi


@app.route("/",methods=["GET","POST"])
def get_books(url=None):
    # test = GetBookList("test","test2")
    search = SearchInApi()
    # results=test.get_response()
    if request.method == "GET":
        test = GetBookList("test", "test2")
        results = test.get_response()
        return render_template("list_of_books_view.html",form=results,search=search)
    elif request.method == "POST":
        test = GetBookList(request.form.get("search"), "test2")
        results2 = test.get_response()
        print("tutaj")
        print(request.form.get("search"))
        return render_template("list_of_books_view.html", form=results2, search=search)
        # test = GetBookList()

@app.route("/imports",methods = ['POST'] )
def import_books():
    print("tutaj")
    print(request.args)