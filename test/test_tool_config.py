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

    with pytest.raises(ConfigParser.MissingSectionHeaderError):
        sc_no_section_header = SearchConfiguration(NO_SECTION_HEADER)
        sc_no_section_header.get_search_config()

def test_parse_simple():
    sc = SearchConfiguration(SIMPLE)
    sc.get_search_config()
    sc.parse()

    assert len(sc.connectors) == 1
    assert isinstance(sc.connectors[0], PSQLConnector)

def test_parse_unknown(capsys):
    sc = SearchConfiguration(UNKNOWN)
    sc.get_search_config()
    sc.parse()
    out, err = capsys.readouterr()

    assert len(sc.connectors) == 0
    assert "Skipping " in err

def test_parse_psql_mysql():
    sc = SearchConfiguration(PSQL_MYSQL)
    sc.get_search_config()
    sc.parse()

    assert len(sc.connectors) == 2
    assert isinstance(sc.connectors[0], PSQLConnector)
    assert isinstance(sc.connectors[1], MySQLConnector)

