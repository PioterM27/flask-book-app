import json

from pathlib import Path
from book_managment_app import app, db
from book_managment_app.models.Book import Book


def load_json_data(file_name: str) -> list:
    json_path = Path(__file__).parent.parent / "samples" / file_name
    with open(json_path) as file:
        data_json = json.load(file)
    return data_json


@app.cli.group()
def db_manage():
    """Database managment commands"""
    pass


@db_manage.command()
def remove_data():
    """Remove all data from the database"""
    try:
        db.session.execute("DELETE FROM books")
        db.session.execute("ALTER TABLE books AUTO_INCREMENT = 1")
        db.session.commit()
        print("Data has been successfully removed from the database")
    except Exception as exc:
        print("Unexpected error: {}".format(exc))
