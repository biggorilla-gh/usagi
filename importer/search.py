from lib.solr import *
import sys

solr = solr()

res = solr.search("all_txt_ng:%s" % solr_sanitize(sys.argv[1]))

print("%d Documents found." % res.hits)
for i, value in enumerate(res.docs):
    fv = [ "\t%s : %s" % (k, str(v)) for k, v in value.items()]
    print("%d: %s\n" % (i, "\n".join(fv)))

