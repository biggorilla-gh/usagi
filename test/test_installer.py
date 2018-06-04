import os
import csv
from installer.run import main
from lib.database import Document, Database
from lib.solr import Solr
import pytest

TESTDIR = os.path.dirname(os.path.abspath(__file__))
SIMPLE = TESTDIR + "/simple/search.ini"
TEST_META_FILE = "/tmp/simple.meta"


# Run this test at the very begging to set up solr
@pytest.mark.run(order=1)
def test_installer_simple():
    silentremove(TEST_META_FILE)

    error_code = main([SIMPLE, TEST_META_FILE])

    assert error_code == 0

    # check metadata file
    meta = []
    with open(TEST_META_FILE) as metadata:
        reader = csv.reader(metadata)
        products_table_exists = 0
        for row in reader:
            if row[1] == 'Products':
                products_table_exists += 1
                assert "xmin" in row[2]
                assert "productDescription" in row[2]
            meta.append(row)
        assert len(meta) == 8
        assert products_table_exists == 1

    # check solr
    s = Solr()
    res = s.list()
    assert res["hits"] == 8
    assert len(res["docs"]) == 8

    # check database
    db = Database()
    db.connect()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM documents ORDER BY ID")
    documents = cursor.fetchall()
    assert len(documents) == len(meta)
    for i in range(0, len(meta)):
        assert documents[i]["universal_id"] == "ClassicModels.public." + meta[i][1]

    cursor.execute("SELECT * FROM filters ORDER BY ID")
    filters = cursor.fetchall()
    assert len(filters) == 2
    assert filters[0]["name"] == "ClassicModels"
    assert filters[1]["name"] == "public"
    assert filters[0]["id"] == filters[1]["parent_id"]

import errno

def silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occurred
