from lib.solr import *
from lib.database import *
import json

s = Solr()
doc = Document()

while True:
    print ">> ",
    raw = raw_input()
    if not raw:
        raw = ""
    args = raw.split()
    command = args.pop(0) if len(args) else ""
    if command == "" or command == "help":
        print """print helps...
        """
        continue
    if command == "quit":
        break
    if command == "search":
        q = args[0] if len(args) > 0 else None
        path = args[1] if len(args) > 1 else None
        res = s.search(q, path)
        print "hits: " + str(res["hits"])
        for d in res["docs"]:
            print "<" + d.get("universal_id") + ">",
            print "  " + d.get("title"),
            if d.get("path"):
                print "  " + d.get("path")
        print "\n"
    if command == "total":
        res = s.list()
        print "total: " + str(res["hits"])
    if command == "filters":
        depth = int(args[0]) if len(args) else 0
        res = doc.filters(0, depth)
        def printTree(t, indent = 0):
            for n in t:
                for i in range(0, indent):
                    print "  ",
                print str(n["id"]) + ":" + n["name"]
                if "children" in n:
                    printTree(n["children"], indent+1)
        printTree(res)

