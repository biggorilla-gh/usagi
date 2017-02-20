import os
import pytest
import ConfigParser
from installer.tool_config import *

TESTDIR = os.path.dirname(os.path.abspath(__file__))
UNKNOWN = TESTDIR + "/expected_failures/unknown_data_store.ini"
NO_SECTION_HEADER = TESTDIR + "/expected_failures/missing_section_header.ini"
SIMPLE = TESTDIR + "/simple/search.ini"
PSQL_MYSQL = TESTDIR + "/psql_mysql/search.ini"

def test_get_search_config():
    sc_simple = SearchConfiguration(SIMPLE)
    sc_simple.get_search_config()

    assert len(sc_simple.config.sections()) > 0

    with pytest.raises(ConfigParser.MissingSectionHeaderError):
        sc_no_section_header = SearchConfiguration(NO_SECTION_HEADER)
        sc_no_section_header.get_search_config()


def test_parse_simple():
    sc = SearchConfiguration(SIMPLE)
    sc.get_search_config()
    sc.parse()

    assert len(sc.handles) == 1
    assert isinstance(sc.handles[0], PSQLHandle)

    pg_handle = sc.handles[0]

    assert pg_handle.name == 'ClassicModels'
    assert "host=localhost" in pg_handle.dsn
    assert "port=5432" in pg_handle.dsn
    assert "user=xfeng" in pg_handle.dsn
    assert "dbname=classicmodels" in pg_handle.dsn


def test_parse_unknown(capsys):
    sc = SearchConfiguration(UNKNOWN)
    sc.get_search_config()
    sc.parse()
    out, err = capsys.readouterr()

    assert len(sc.handles) == 0
    assert "Skipping " in err


def test_parse_psql_mysql():
    sc = SearchConfiguration(PSQL_MYSQL)
    sc.get_search_config()
    sc.parse()

    assert len(sc.handles) == 2
    assert isinstance(sc.handles[0], PSQLHandle)
    assert isinstance(sc.handles[1], MySQLHandle)

