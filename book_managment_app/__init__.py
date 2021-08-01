from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_bootstrap import Bootstrap
# from book_managment_app.models import Book

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)



# results = db.session.execute('show databases')
# for row in results:
#     print(row)

from book_managment_app.views import books
from book_managment_app.models import Book
