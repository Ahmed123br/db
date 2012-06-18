import sqlite3

import db
from db.drivers import Driver

from collections import namedtuple


def _namedtuple_factory(cursor, row):
    fields = [col[0] for col in cursor.description]
    Row = namedtuple("Row", fields)
    return Row(*row)


def connect(*args, **kwargs):
    """Wraps sqlite3.connect forcing the options required for a
       db style connection to work.  As of this writing that consists
       of installing a NamedTupleCursor factory but may grow more involved
       over time as things change.
    """

    conn = sqlite3.connect(*args, **kwargs)
    conn.row_factory = _namedtuple_factory
    return conn


def register(conn_string, name=None, **kwargs):
    driver = Sqlite3Driver(conn_string, **kwargs)
    return db.drivers.register(driver, name)


class Sqlite3Driver(Driver):

    PARAM_STYLE = "qmark"

    def __init__(self, conn_string, **kwargs):
        self.conn_string = conn_string
        self.conn = connect(self.conn_string, **kwargs)

    def connect(self):
        return self.conn