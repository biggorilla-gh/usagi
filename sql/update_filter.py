from lib.database import *

def find_or_insert(cursor, parent_id, name):
    cursor.execute("select id from filters where parent_id = %s and name = %s", (parent_id, name))
    row = cursor.fetchone()
    if not row:
        cursor.execute("insert into filters (parent_id, name) values (%s, %s)", (parent_id, name))
        return find_or_insert(cursor, parent_id, name)
    else:
        return row["id"]

db = Database()
db.connect()
cursor = db.cursor()

cursor.execute("select distinct path from documents where path is not null")

for row in cursor.fetchall():
    path = row["path"].split("/")
    parent_id = 0
    for p in path:
        parent_id = find_or_insert(cursor, parent_id, p)

cursor.close()
db.commit()
db.close()

