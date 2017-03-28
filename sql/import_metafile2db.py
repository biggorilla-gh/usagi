# -*- coding: utf-8 -*-
from lib.database import Document
import sys
import csv

meta_data_file = sys.argv[1]
doc = Document()

with open(meta_data_file) as metadata:
    reader = csv.reader(metadata)
    for row in reader:
        doc.create(row[0], row[1])

doc.close()


