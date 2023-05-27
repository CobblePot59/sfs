from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from hashids import Hashids
from flask_dropzone import Dropzone

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
from models import *

dropzone = Dropzone(app)
hashids = Hashids(min_length=64, salt=app.config['SECRET_KEY'])

from views import *

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
