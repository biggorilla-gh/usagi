import sys,os
sys.path.append(os.pardir + "/importer")

from flask import Flask, request
from solr import *
import json

solr = solr()

app = Flask(__name__)

@app.route("/api/search")
def search():
    q = request.args.get('q')
    if not q:
        return json.dumps({
            "hits": 0,
            "docs": [],
        })
    res = solr.search("all_txt_ng:%s" % solr_sanitize(q))
    docs = [{"title": d["title_s"]} for d in res.docs]
    return json.dumps({
        "hits": res.hits,
        "docs": docs,
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8085)

