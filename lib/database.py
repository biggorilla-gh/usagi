import psycopg2
from psycopg2.extras import DictCursor
from config.config import *

class Database:
    def __init__(self):
        self.connected = False

    def connect(self):
        if self.connected:
            return
        C = CONFIG['DB']
        self.con = psycopg2.connect(
            host=C['host'],
            port=C['port'],
            dbname=C['name'],
            user=C['user'],
            password=C['pass'])
        self.connected = True

    def cursor(self):
        return self.con.cursor(cursor_factory=DictCursor)

    def commit(self):
        self.con.commit()

    def close(self):
        self.con.close()
        self.connected = False

    def __enter__(self):
        self.cursor = self.cursor()
        return self.cursor

    def __exit__(self):
        self.cursor.close()
        self.cursor = None
        self.commit()

class Document():
    def __init__(self):
        self.db = Database()
        self.db.connect()
        self.cursor = self.db.cursor()
        self.import_statement = "INSERT INTO documents (universal_id, title, keywords, path) VALUES (%s, %s, %s, %s)"

    def clear(self):
        self.cursor.execute("truncate table documents")

    def create(self, universal_id, title, keywords, path=None):
        self.cursor.execute(self.import_statement, (universal_id, title, keywords, path))

    def filters(self, parent_id = 0, depth = 1):
        query = "select * from filters where parent_id = %s"
        self.cursor.execute(query, (parent_id,))
        fs = self.cursor.fetchall()
        fs = [dict(f) for f in fs]
        if depth > 1:
            for f in fs:
                f["children"] = self.filters(f["id"], depth-1)
        return fs

    def close(self):
        self.cursor.close()
        self.db.commit()
        self.db.close()

