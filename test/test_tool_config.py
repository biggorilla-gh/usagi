import os
import pytest
import ConfigParser
from installer.tool_config import *

TESTDIR = os.path.dirname(os.path.abspath(__file__))
UNKNOWN = TESTDIR + "/expected_failures/unknown_data_store.ini"
NO_SECTION_HEADER = TESTDIR + "/expected_failures/missing_section_header.ini"
PG_PORT_NOT_INT = TESTDIR + "/expected_failures/pg_port_not_int.ini"
MY_PORT_NOT_INT = TESTDIR + "/expected_failures/my_port_not_int.ini"
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
    parsed = sc.parse()

    assert parsed
    assert len(sc.handles) == 1
    assert isinstance(sc.handles[0], PSQLHandle)

    pg_handle = sc.handles[0]

    assert pg_handle.name == 'ClassicModels'
    assert "host=localhost" in pg_handle.dsn
    assert "port=5432" in pg_handle.dsn
    assert "user=classic_user" in pg_handle.dsn
    assert "dbname=classicmodels" in pg_handle.dsn


def test_parse_unknown(capsys):
    sc = SearchConfiguration(UNKNOWN)
    sc.get_search_config()
    parsed = sc.parse()
    out, err = capsys.readouterr()

    assert parsed == False
    assert "non-supported" in err


def test_parse_pg_port_not_int(capsys):
    sc = SearchConfiguration(PG_PORT_NOT_INT)
    sc.get_search_config()
    parsed = sc.parse()
    out, err = capsys.readouterr()

    assert parsed == False
    assert "Unexpected value of \"port\" " in err


def test_parse_my_port_not_int(capsys):
    sc = SearchConfiguration(MY_PORT_NOT_INT)
    sc.get_search_config()
    parsed = sc.parse()
    out, err = capsys.readouterr()

    assert parsed == False
    assert "Unexpected value of \"port\" " in err


def test_parse_psql_mysql():
    sc = SearchConfiguration(PSQL_MYSQL)
    sc.get_search_config()
    parsed = sc.parse()

    assert parsed

    assert len(sc.handles) == 2
    assert isinstance(sc.handles[0], PSQLHandle)
    assert isinstance(sc.handles[1], MySQLHandle)

    pg_handle = sc.handles[0]

    assert pg_handle.name == 'ClassicModels'
    assert "host=localhost" in pg_handle.dsn
    assert "port=5432" in pg_handle.dsn
    assert "user=classic_user" in pg_handle.dsn
    assert "dbname=classicmodels" in pg_handle.dsn

    my_handle = sc.handles[1]

    assert my_handle.name == 'employees sakila sportsdb'
    assert ('host', 'localhost') in my_handle.params.items()
    assert ('port', 3306) in my_handle.params.items()
    assert isinstance(my_handle.params['port'], int)
    assert ('user', 'root') in my_handle.params.items()
    assert ['employees', 'sakila', 'sportsdb'] == my_handle.databases

