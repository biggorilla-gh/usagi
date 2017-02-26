# -*- coding: utf-8 -*-
from solr import *
import sys
import csv

meta_data_file = sys.argv[1]
solr = solr()

datalist = []
with open(meta_data_file) as metadata:
    reader = csv.DictReader(metadata)
    for row in reader:
        datalist.append({
            "title_s": row['title'],
            "all_txt_ng": row['content'],
        })

solr.delete(q="*:*")
solr.add(datalist)

