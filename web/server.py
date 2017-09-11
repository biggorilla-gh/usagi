from flask import Flask, request, render_template
from lib.solr import *
from lib.database import *
import json

s = Solr()
doc = Document()

app = Flask(__name__)

@app.route("/")
def index():
    q = request.args.get('q', "")
    path = request.args.get('path', "")
    res = s.search(q, path)
    return render_template("index.html", res=res)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8085)

