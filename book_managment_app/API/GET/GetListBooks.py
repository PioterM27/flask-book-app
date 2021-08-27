import parser

from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from book_managment_app import app, api, db
from book_managment_app.models.Book import Book
from sqlalchemy import exc


class GetListBooks(Resource):
    def get(self):
        books = _get_books_from_db()
        if books[0] is not exc.SQLAlchemyError:
            book_list = [book.return_json() for book in books]
            return jsonify(book_list)
        else:
            return jsonify({'status': 500, 'data': books[1]})


class GetBook(Resource):
    def get(self, filters, value):
        book = _get_book_from_db_using_filter(filters,value)
        if book[0] is not Exception:
            book_list = [book.return_json() for book in book]
            return jsonify(book_list)
        else:
            return jsonify({'status': 500, 'data': book[1]})


def _get_books_from_db():
    try:
        books = Book.query.all()
    except exc.SQLAlchemyError:
        message = "Cannot conect with db check your connection string"
        return exc.SQLAlchemyError, message
    else:
        return books


def _get_book_from_db_using_filter(filters, value):
    try:
        if filters == 'title':
            filter_books = Book.query.filter(Book.title == value).all()
        elif filters == 'author':
            filter_books = Book.query.filter(Book.author == value).all()
        elif filters == 'language':
            filter_books = Book.query.filter(Book.publication_language == value).all()
        if filter_books == []:
            raise Exception('Nothing was found')
    except Exception as ex:
        message = str(ex.args)
        return Exception, message
    else:
        return filter_books


api.add_resource(GetListBooks, "/test")
api.add_resource(GetBook, "/test/<filters>/<value>")
