from flask import Flask, request
from lib.solr import *
from lib.database import *
import json

s = Solr()
doc = Document()

app = Flask(__name__)

@app.route("/api/search")
def search():
    q = request.args.get('q')
    path = request.args.get('path')
    res = s.search(q, path)
    return json.dumps(res)

@app.route("/api/filters")
def filters():
    depth = int(request.args.get("depth", 0))
    res = doc.filters(0, depth)
    return json.dumps(res)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8085)

