from flask import Flask, jsonify
from flask_restful import Resource, Api
from book_managment_app import app, api, db
from book_managment_app.models.Book import Book


class GetBooks(Resource):
    def get(self):
        books = Book.query.all()
        book_list = []
        for book in books:
            book_list.append(book.return_json())
        return jsonify({"status": 200, "data": book_list})

    def put(self):
        return {"dobrze": "jest"}


api.add_resource(GetBooks, "/test")
