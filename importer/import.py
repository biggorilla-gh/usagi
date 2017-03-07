# -*- coding: utf-8 -*-
from solr import *
import sys
import csv

meta_data_file = sys.argv[1]
solr = solr()

datalist = []
with open(meta_data_file) as metadata:
    reader = csv.reader(metadata)
    for row in reader:
        datalist.append({
            "title_s": row[0],
            "all_txt_ng": row[1],
        })

solr.delete(q="*:*")
solr.add(datalist)

