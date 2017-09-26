# -*- coding: utf-8 -*-
from db import *
import pysolr
import sys
import json
import time
import re
from util import *

print("prepare...")
solr = solr()
datalist = []
paths = json.load(open("RegionPath2.txt"))


def add(data):
    global datalist
    datalist.append(data)
    if len(datalist) > 100:
        solr.add(datalist)
        datalist = []


def commit():
    global datalist
    if len(datalist):
        solr.add(datalist)
    datalist = []


def infrate_countries(p, data, n):
    matches = []
    if n == 3:
        return matches
    # まずは部分マッチしているリストを列挙する
    for path in p:
        found = False
        for name in path["names"]:
            if -1 != data.find(name.lower()):
                found = True
                break
        if found:
            matches.extend(path["names"])
        if "children" in path:
            matches.extend(infrate_countries(path["children"], data, n+1))
    return matches

cur = database()
cur.execute("select * from publications")
solr.delete(q="*:*")
print("insert...")
n = 0
start = time.time()
for row in cur:
    keywords = " ".join(row["keywords"].split(";")) if row["keywords"] else ""
    countries = infrate_countries(paths, " ".join(
        map(str, [row["title"], row["description"], keywords, row["spatial_bounds"]])).lower(), 1)
    countries = " ".join(countries)
    loc = row["spatial_bounds"]
    if loc and loc[:1] == '{':
        j = json.loads(loc)
        t = j["type"]
        if t == 'Point':
            loc = geojson_dumps({"type": t, "coordinates": normalize(j["coordinates"])})
        elif t == 'Polygon':
            j["coordinates"] = normalize_polygon_coordinates(j["coordinates"])
            loc = geojson_dumps(j)
        else:
            pass
    elif loc:
        if re.match(r'^[-0-9.,]$', loc):
            splited = [int(v.strip()) for v in loc.split(",")]
            if len(splited) == 2:
                loc = {"type": "Point", "coordinates": normalize(splited)}
            elif len(splited) == 4:
                loc = {"type": "Polygon", "coordinates": [
                    [
                        normalize([splited[0], splited[1]]),
                        normalize([splited[1], splited[1]]),
                        normalize([splited[0], splited[3]]),
                        normalize([splited[1], splited[3]]),
                        normalize([splited[0], splited[1]]),
                    ]
                ]}
            else:
                print("point is {}".format(len(splited)))
                print(splited)
        else:
            loc = None
    else:
        loc = None

    add({
        "id_l": row["id"],
        "category_s": row["category"],
        "title_s": row["title"],
        "description_s": row["description"],
        "publisher_s": row["publisher"],
        "keywords_s": row["keywords"],
        "all_txt_en": " ".join(map(str, [row["category"], row["title"], row["description"], row["publisher"], keywords, countries])),
        "all_txt_ng": " ".join(map(str, [row["category"], row["title"], row["description"], row["publisher"], keywords, countries])),
        "spatial_bounds": loc,
        "spatial_bounds_s": row["spatial_bounds"],
        "issue_date": row["issue_date"],
        "crawl_time": row["crawl_time"],
        "last_update_date": row["last_update_date"],
    })
    n += 1
    if (n % 1000) == 0:
        print("{} ({}s)".format(n, time.time() - start))
        start = time.time()

commit()
