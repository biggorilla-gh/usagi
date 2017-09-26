# -*- coding: utf-8 -*-
from db import *
import pysolr
import sys

solr = solr()

datalist = []


def add(data):
    global datalist
    datalist.append(data)
    if len(datalist) > 500:
        solr.add(datalist)
        datalist = []


def commit():
    global datalist
    if len(datalist):
        solr.add(datalist)
    datalist = []

cur = database()
cur.execute("select * from publications")
solr.delete(q="*:*")

n = 0
for row in cur:
    keywords = " ".join(row["keywords"].split(";")) if row["keywords"] else ""
    add({
        "id_l": row["id"],
        "category_s": row["category"],
        "title_s": row["title"],
        "description_s": row["description"],
        "publisher_s": row["publisher"],
        "keywords_s": row["keywords"],
        "all_txt_en": " ".join(map(str, [row["category"], row["title"], row["description"], row["publisher"], keywords])),
        "all_txt_ng": " ".join(map(str, [row["category"], row["title"], row["description"], row["publisher"], keywords])),
    })
    n += 1
    if (n % 1000) == 0:
        print(n)

commit()
