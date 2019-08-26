#!/usr/bin/env python

import sqlite3

from flask import Flask

from book import models
from book.views import bp


app = Flask(__name__)


def init_app(app):
    app.run(host='0.0.0.0', debug=False)
    models.init_db()
    app.register_blueprint(bp)


init_app(app)
