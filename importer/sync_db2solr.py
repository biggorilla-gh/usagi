# -*- coding: utf-8 -*-
from lib.database import Database
from lib.solr import *

solr = solr()
db = Database()

db.connect()
cursor = db.cursor()
cursor.execute("SELECT * FROM documents")

datalist = []
for row in cursor.fetchall():
    datalist.append({
        "title_s": row["title"],
        "all_txt_ng": row["keywords"],
    })

cursor.close()
db.close()

solr.delete(q="*:*")
solr.add(datalist)

