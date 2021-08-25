import requests
from book_managment_app.models.Book import Book


class GetBookList:
    """Util class to handled connection and response form Google Book Api"""

    def __init__(self, key, filter_by):
        self.filter_by = filter_by
        self.key = key
        self.URL = f"https://www.googleapis.com/books/v1/volumes?q={self.filter_by}+{self.key}:keyes&key="

    def get_response(self):
        response = requests.get(url=self.URL)
        list_of_books = []
        test = response.json()
        for key in test.get("items", []):
            book = Book()
            book.title = key.get("volumeInfo").get("title")
            book.author = key.get("volumeInfo").get("authors")
            book.number_of_pages = key.get("volumeInfo").get("pageCount")
            book.publication_date = key.get("volumeInfo").get("publishedDate")
            book.publication_language = key.get("volumeInfo").get("language")
            book.book_cover_link = key.get("volumeInfo").get("previewLink")
            book.isbn = (
                key.get("volumeInfo").get("industryIdentifiers")[0].get("identifier")
            )
            list_of_books.append(book)
        return list_of_books
