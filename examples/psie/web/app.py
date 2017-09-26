# -*- coding: utf-8 -*-
from flask import Flask, request, render_template
import pysolr
import json
from db import *
from pagenator import *
import requests
import pycountry
import sys
import re
from util import *
from geomap import GeoMap
from datetime import datetime

app = Flask(__name__, static_folder="static", static_url_path="")
solr = solr()
m = GeoMap("data.list")


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)

def inflate_geonames(query):
    keywords = []
    lq = query
    lq = lq.lower()
    for c in pycountry.countries:
        cname = c.name.lower()
        match = -1 != lq.find(cname)
        if match:
            keywords.append(cname)
        for s in pycountry.subdivisions.get(country_code=c.alpha_2):
            sname = s.name.lower()
            if match:
            #    keywords.append(sname)
                pass
            else:
                if -1 != lq.find(sname):
                    keywords.append(cname)
                    keywords.append(sname)
    return keywords

def countries():
    data = []
    for c in pycountry.countries:
        country = {
            "name": c.name,
            "children": [s.name for s in pycountry.subdivisions.get(country_code=c.alpha_2)],
        }
        data.append(country)
    return data

@app.route("/")
def top():
    global solr
    q = request.args.get("q")
    page = int(request.args.get("p", 1)) - 1
    docs = []
    hits = 0
    size = 10
    current = page * size
    country = request.args.get("country")
    subdivision = request.args.get("subdivision")

    if q or country:
        geonames = [v for v in [country, subdivision] if v]
        qt = q if q else ""
        for n in geonames:
            r = re.compile(re.escape(n), re.IGNORECASE)
            qt = r.sub("", qt)
        query = []
        if qt:
            query.append("(" + " AND ".join(["all_txt_ng:" + solr_sanitize(w.strip()) for w in qt.strip().split()]) + ")")
        if geonames:
            query.append("(" +
                         " AND ".join(["all_txt_ng:" + solr_sanitize(n) for n in geonames]) + ")")
        print(" AND ".join(query))
        res=solr.search(" AND ".join(query), start=current, rows=size)
        docs=res.docs
        hits=res.hits

    pages=Pagenator().pagenation(hits, size, current)
    return render_template("index.html", docs=docs, q=q, hits=hits, pages=pages, countries=json.dumps(countries()), country=country, subdivision=subdivision)


@app.route("/map")
def map():
    global solr
    q = request.args.get("q")
    page = int(request.args.get("p", 1)) - 1
    docs = []
    hits = 0
    size = 10
    current = page * size
    _geo = request.args.get("geo")
    from_date = request.args.get("from")
    to_date = request.args.get("to")

    if q or _geo or from_date or to_date:
        query = []
        if q:
            query.append("(" + " AND ".join(["all_txt_ng:" + solr_sanitize(w.strip()) for w in q.strip().split()]) + ")")
        else:
            query.append("*:*")
        res = {}

        if from_date:
            query.append("(issue_date:[" + solr_sanitize(from_date) + "T00:00:00.000Z TO *])")
        if to_date:
            query.append("(issue_date:[* TO " + solr_sanitize(to_date) + "T23:59:59.999Z])")
        if _geo:
            geo = json.loads(_geo)
            geo["coordinates"] = normalize_polygon_coordinates(geo["coordinates"])
            geo = geojson_dumps(geo)
            res=solr.search(" AND ".join(query), start=current, rows=size, fq="{!field f=spatial_bounds}Intersects("+geo+")")
            print(" AND ".join(query))
            print("{!field f=spatial_bounds}Intersects("+geo+")")
        else:
            res=solr.search(" AND ".join(query), start=current, rows=size)
        docs=res.docs
        hits=res.hits

    pages=Pagenator().pagenation(hits, size, current)
    return render_template("map.html", docs=docs, q=q, hits=hits, pages=pages, geo=_geo, f=from_date, to=to_date)

@app.route("/map_suggest")
def map_suggest():
    global m
    q = request.args.get("q")
    data = m.findByName(q)
    return json.dumps(data)

@app.route("/map_find")
def map_find():
    global m
    loc = request.args.get("loc")
    print(loc)
    loc = [float(l) for l in loc.split(",")]
    data = m.findByLocation(loc)
    if len(data):
      return json.dumps(data[0])
    return "{}"

@app.route("/detail/<pid>")
def detail2(pid):
    db=database()
    db.execute("""
        select
            *
        from
            publications
        where id = %s
    """, (str(pid),))
    data=db.fetchone()
    db.execute("""
        select
             l.label,
             u.url
        from
             links l
        left join urls u
             on l.url_id = u.id
        where l.publication_id = %s
    """, (str(pid),))
    links = db.fetchall()
    return render_template("detail.html", publication=data, links=links, re=re)


def detail(pid):
    db=database()
    db.execute("""
        select
            *
        from
            publications
        where id = %s
    """, (str(pid),))
    publication=db.fetchone()

    db.execute("""
        select
             l.label,
             u.url
        from
             links l
        left join urls u
             on l.url_id = u.id
        where l.publication_id = %s
    """, (str(pid),))
    links = db.fetchall()
    db.close()
    return render_template("detail.html", publication=publication, links=links)


def find_or_append(data, value):
    if value in data:
        return data.index(value)
    else:
        data.append(value)
        return len(data) - 1


@app.route("/graph/<pid>")
def graph(pid):
    data=[]
    root=requests.get("http://52.197.249.40:8082?id={}".format(pid)).json()
    data.extend([{"source": pid, "target": r["S"], "score": r["F"]}
                 for r in root])
    for s in root:
        res=requests.get(
            "http://52.197.249.40:8082?id={}".format(s["S"])).json()
        data.extend(
            [{"source": s["S"], "target": r["S"], "score": r["F"]} for r in res])

    nodes=[]
    links=[]
    for i, d in enumerate(data):
        si=find_or_append(nodes, d["source"])
        ti=find_or_append(nodes, d["target"])
        links.append({"source": si, "target": ti, "score": d["score"]})
    nodes=[{"name": v} for v in nodes]

    return render_template("graph.html", data=json.dumps({
        "nodes": nodes,
        "links": links
    }))

def convert_docs(docs):
    key_list = {
        "id": "id_l",
        "category": "category_s",
        "title": "title_s",
        "description": "description_s",
        "publisher": "publisher_s",
        "spatial_bounds": "spatial_bounds",
        "issue_date": "issue_date",
    }
    results = []
    for d in docs:
        converted = {}
        for k1, k2 in key_list.items():
            if k2 in d:
                converted[k1] = d[k2]
        if "issue_date" in converted:
            converted["issue_date"] = converted["issue_date"][0]
        results.append(converted)
    return results

@app.route("/api/search")
def api_search():
    global solr
    q = request.args.get("q")
    page = int(request.args.get("p", 1)) - 1
    docs = []
    hits = 0
    size = 10
    current = page * size
    _geo = request.args.get("geo")
    from_date = request.args.get("from")
    to_date = request.args.get("to")
    include_pages = request.args.get("ip")

    if q or _geo or from_date or to_date:
        query = []
        if q:
            query.append("(" + " AND ".join(["all_txt_ng:" + solr_sanitize(w.strip()) for w in q.strip().split()]) + ")")
        else:
            query.append("*:*")
        res = {}

        if from_date:
            query.append("(issue_date:[" + solr_sanitize(from_date) + "T00:00:00.000Z TO *])")
        if to_date:
            query.append("(issue_date:[* TO " + solr_sanitize(to_date) + "T23:59:59.999Z])")
        if _geo:
            geo = json.loads(_geo)
            geo["coordinates"] = normalize_polygon_coordinates(geo["coordinates"])
            geo = geojson_dumps(geo)
            res=solr.search(" AND ".join(query), start=current, rows=size, fq="{!field f=spatial_bounds}Intersects("+geo+")")
        else:
            res=solr.search(" AND ".join(query), start=current, rows=size)
        docs=res.docs
        hits=res.hits

    pages=Pagenator().pagenation(hits, size, current)
    docs = convert_docs(docs)
    res = {
        "docs": docs,
        "hits": hits,
    }
    if include_pages:
        res["pages"] = pages
    return json.dumps(res)

@app.route("/api/detail/<pid>")
def api_detail(pid):
    db=database()
    db.execute("""
        select
            *
        from
            publications
        where id = %s
    """, (str(pid),))
    publication=db.fetchone()
    db.execute("""
        select
           l.label,
           d.filename, d.content_type, d.status_code, d.crawl_time,
           c.id, c.file_type, c.size
        from
            publications p
        inner join links l
            on l.publication_id = p.id
        inner join downloads d
            on d.url_id = l.id
        inner join components c
            on c.id = d.component_id
        where p.id = %s
    """, (str(pid),))
    components=db.fetchall()
    for c in components:
        db.execute("""
            select
                s.*
            from
                subcomponents s
            where s.parent_id = %s
        """, (str(c["id"]),))
        c["subcomponents"]=db.fetchall()
    db.close()
    return json.dumps({
        "publication": publication,
        "components": components,
    }, cls=DateTimeEncoder)

if __name__ == "__main__":
    port=sys.argv[1]
    app.run(host="0.0.0.0", port=port)
