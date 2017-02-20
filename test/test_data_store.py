import os
import ast
import csv
from installer.tool_config import *

TESTDIR = os.path.dirname(os.path.abspath(__file__))
SIMPLE = TESTDIR + "/simple/search.ini"
PSQL_MYSQL = TESTDIR + "/psql_mysql/search.ini"

def test_copy_raw_meta_data():
    silentremove("/tmp/simple.meta")

    sc = SearchConfiguration(SIMPLE)
    sc.get_search_config()
    sc.parse()
    pg_handle = sc.handles[0]

    pg_handle.connect()
    pg_handle.copy_raw_meta_data("/tmp/simple.meta")
    pg_handle.close()

    with open("/tmp/simple.meta") as metadata:
        reader = csv.DictReader(metadata)
        n_tables = 0
        for row in reader:
            n_tables += 1
            if row['table_name'] == 'Products':
                col2type = ast.literal_eval(row['col_to_type'])
                assert col2type['quantityInStock'] == 'smallint'
        assert n_tables == 8


import errno

def silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occurred
