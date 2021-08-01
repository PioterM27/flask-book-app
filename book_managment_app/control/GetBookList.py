import requests
import json
from book_managment_app.models.Book import Book

class GetBookList:
    # URL = f"https://www.googleapis.com/books/v1/volumes?q={Hobbit}+inauthors:keyes&key=AIzaSyCsgA_L-2RWCz6aTyKczoohqFasDls80_g"
    def __init__(self,api_key,filter_by):
        self.filter_by = filter_by
        self.api_key = api_key
        self.URL = f"https://www.googleapis.com/books/v1/volumes?q={self.api_key}+inauthors:keyes&key=AIzaSyCsgA_L-2RWCz6aTyKczoohqFasDls80_g"
    def get_response(self):
        response=requests.get(url=self.URL)
        print(self.URL)
        response_list = []
        list_of_books = []
        test=response.json()
        # print(test)
        # print(response['items']["volumeInfo"]["authors"])
        for key in test.get('items'):
            book = Book()
            book.title = key.get('volumeInfo').get('title')
            book.author = key.get('volumeInfo').get('authors')
            book.number_of_pages = key.get('volumeInfo').get('pageCount')
            list_of_books.append(book)
            # book.number_of_pages = key["volumeInfo"]["pageCount"]
            # book.isbn = key["volumeInfo"]["pageCount"]
            # book.book_cover_link
            # book.publication_date = key["volumeInfo"]["publishDate"]
            # book.publication_language
        return list_of_books

