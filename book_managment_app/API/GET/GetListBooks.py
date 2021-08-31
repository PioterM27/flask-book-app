import parser
import json

from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from book_managment_app import app, api, db
from book_managment_app.models.Book import Book
from book_managment_app.control.GetBookList import GetBookList
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
    def post(self,filters,value):
        required_post_args = reqparse.RequestParser()
        required_post_args.add_argument("ala", type=str,required=True)
        args = required_post_args.parse_args()
        add_book_object_to_db = Book(**args)
        return jsonify({'status': 200, 'data':args,'message': 'New book has been added to Your library'})


class AddBook(Resource):
    def get(self):
        pass

    def post(self):
        required_post_args = reqparse.RequestParser()
        required_post_args.add_argument("title", type=str, required=True)
        required_post_args.add_argument("author", type=str, required=True)
        required_post_args.add_argument("number_of_pages", type=int, required=True)
        required_post_args.add_argument("publication_language", type=str, required=True)
        required_post_args.add_argument("publication_date", type=str, required=True)
        required_post_args.add_argument("book_cover_link", type=str, required=True)
        required_post_args.add_argument("isbn", type=str, required=True)
        args = required_post_args.parse_args()
        add_book_object_to_db = Book(**args)
        _add_to_db(add_book_object_to_db)
        return jsonify({'status': 200, 'data': args, 'message': 'New book has been added to Your library'})


class GetBookFromApi(Resource):
    def get(self, key_word, key):
        book_from_api = GetBookList(key_word,key)
        data = book_from_api.get_response()
        return data


def _get_books_from_db():
    try:
        books = Book.query.all()
    except exc.SQLAlchemyError:
        message = "Cannot conect with db check your connection string"
        return exc.SQLAlchemyError, message
    else:
        return books


def _add_to_db(book_object):
    db.session.add(book_object)
    db.session.commit()


def _get_book_from_db_using_filter(filters, value):
    try:
        if filters == 'title':
            filter_books = Book.query.filter(Book.title == value).all()
        elif filters == 'author':
            filter_books = Book.query.filter(Book.author == value).all()
        elif filters == 'language':
            filter_books = Book.query.filter(Book.publication_language == value).all()
        elif filters == ' id':
            filter_books = Book.query.filter(Book.id == value).first()
        if filter_books == []:
            raise Exception('Nothing was found')
    except Exception as ex:
        message = str(ex.args)
        return Exception, message
    else:
        return filter_books


api.add_resource(GetListBooks, "/test")
api.add_resource(GetBook, "/test/<filters>/<value>")
api.add_resource(AddBook, "/test/add")
api.add_resource(GetBookFromApi, "/test/api/<key_word>/<key>")

