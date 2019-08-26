import sqlite3
from contextlib import closing

from validate_email import validate_email


class BookNotFoundError(ValueError):
    pass


class InvalidEmailError(ValueError):
    pass


class RequestNotFoundError(ValueError):
    pass


def dict_factory(cursor, row):
    d = {}
    for i, col in enumerate(cursor.description):
        d[col[0]] = row[i]
    return d


db = sqlite3.connect('hw.sqlite3', check_same_thread=False)
db.row_factory = dict_factory


def init_db():
    db.execute("""CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    email TEXT NOT NULL,
                    UNIQUE(email)
                  );""")
    db.execute("""CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    UNIQUE(title)
                  );""")
    db.execute("""CREATE TABLE IF NOT EXISTS requests (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    book_id INTEGER NOT NULL,
                    timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(user_id, book_id),
                    FOREIGN KEY(user_id) REFERENCES users(id),
                    FOREIGN KEY(book_id) REFERENCES books(id)
                  );""")

    with closing(db.cursor()) as c:
        count = c.execute("""SELECT COUNT(*) AS num FROM books;""").fetchone()
        if count and count['num'] == 0:
            # Seed title list
            with open('books.txt') as f:
                titles = [[line.strip()] for line in f.readlines()]
                c = db.cursor()
                c.executemany("""INSERT INTO books (title) VALUES (?);""",
                              titles)
    db.commit()


def get_one(sql, params=None):
    with closing(db.cursor()) as c:
        c.execute(sql, params)
        return c.fetchone()


def get_all(sql):
    with closing(db.cursor()) as c:
        c.execute(sql)
        return c.fetchall()


def add_one(sql, params=None):
    with closing(db.cursor()) as c:
        c.execute(sql, params)
        rowid = c.lastrowid
        db.commit()
        return rowid


def delete_one(sql, params=None):
    with closing(db.cursor()) as c:
        c.execute(sql, params)
        db.commit()


# Users

def get_user(email):
    user = get_one("""SELECT id, email
                      FROM users
                      WHERE email=?;""", [email])
    return user


def add_user(email):
    if not email or not validate_email(email):
        raise InvalidEmailError(f"Email invalid: {email}")
    return add_one("""INSERT INTO users (email) VALUES (?)""", [email])


# Books

def get_book(title):
    book = get_one("""SELECT id
                      FROM books
                      WHERE title=?;""", [title])
    if book is None:
        raise BookNotFoundError(f"Book with specified title doesn't exist: "
                                f"{title}")
    return book


# Requests

def get_request(id_):
    request = get_one("""SELECT requests.id, title, email, timestamp
                         FROM requests
                         LEFT JOIN books on books.id=requests.book_id
                         LEFT JOIN users on users.id=requests.user_id
                         WHERE requests.id=?;""", [id_])
    if request is None:
        raise RequestNotFoundError(f"Request with specified ID doesn't exist: "
                                   f"{id_}")
    return request


def get_all_requests():
    requests = get_all("""SELECT requests.id, title, email, timestamp
                          FROM requests
                          LEFT JOIN books on books.id=requests.book_id
                          LEFT JOIN users on users.id=requests.user_id;""")
    return requests


def add_request(email, title):
    user = get_user(email)
    if user is None:
        user_id = add_user(email)
    else:
        user_id = user['id']
    book_id = get_book(title)['id']
    return add_one("""INSERT OR IGNORE INTO requests (user_id, book_id) VALUES
                      (?, ?);""", [user_id, book_id])


def delete_request(id_):
    request = get_request(id_)
    return delete_one("""DELETE FROM requests WHERE id=?""", [request['id']])
