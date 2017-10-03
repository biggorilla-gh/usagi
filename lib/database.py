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
        self.cursor.execute("truncate table filters")

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

    def find_or_insert(self, parent_id, name):
        self.cursor.execute("select id from filters where parent_id = %s and name = %s", (parent_id, name))
        row = self.cursor.fetchone()
        if not row:
            self.cursor.execute("insert into filters (parent_id, name) values (%s, %s)", (parent_id, name))
            return self.find_or_insert(parent_id, name)
        else:
            return row["id"]

    def update_filters(self):
        self.cursor.execute("select distinct path from documents where path is not null")

        for row in self.cursor.fetchall():
            path = row["path"].split("/")
            parent_id = 0
            for p in path:
                parent_id = self.find_or_insert(parent_id, p)

