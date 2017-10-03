import os
import csv
from installer.run import main
from lib.database import Document, Database
from lib.solr import Solr

TESTDIR = os.path.dirname(os.path.abspath(__file__))
SIMPLE = TESTDIR + "/simple/search.ini"
PSQL_MYSQL = TESTDIR + "/psql_mysql/search.ini"
DIRECT = TESTDIR + "/direct/search.ini"

def test_installer_simple():
    silentremove("/tmp/simple.meta")

    error_code = main([SIMPLE, "/tmp/simple.meta"])

    assert error_code == 0

    with open("/tmp/simple.meta") as metadata:
        reader = csv.reader(metadata)
        n_tables = 0
        products_table_exists = 0
        for row in reader:
            n_tables += 1
            if row[1] == 'Products':
                products_table_exists += 1
                assert "xmin" in row[2]
                assert "productDescription" in row[2]
        assert n_tables == 8
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
    rows = cursor.fetchall()
    assert len(rows) == 8
    assert rows[0]["universal_id"] == "ClassicModels.public.OrderDetails"
    assert rows[1]["universal_id"] == "ClassicModels.public.Offices"
    assert rows[2]["universal_id"] == "ClassicModels.public.Payments"
    assert rows[3]["universal_id"] == "ClassicModels.public.ProductLines"
    assert rows[4]["universal_id"] == "ClassicModels.public.Customers"
    assert rows[5]["universal_id"] == "ClassicModels.public.Orders"
    assert rows[6]["universal_id"] == "ClassicModels.public.Employees"
    assert rows[7]["universal_id"] == "ClassicModels.public.Products"

    cursor.execute("SELECT * FROM filters ORDER BY ID")
    rows = cursor.fetchall()
    assert len(rows) == 2
    assert rows[0]["name"] == "ClassicModels"
    assert rows[1]["name"] == "public"
    assert rows[0]["id"] == rows[1]["parent_id"]

import errno

def silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occurred
