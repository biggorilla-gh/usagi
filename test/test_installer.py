import os
import csv
from installer.run import main

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


import errno

def silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occurred
