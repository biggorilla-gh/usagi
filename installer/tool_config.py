import sys
import ConfigParser

class SearchConfiguration(object):
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        self.connectors = []

    def get_search_config(self):
        self.config = ConfigParser.SafeConfigParser()
        self.config.read(self.config_file_path)

    def parse(self):
        for name in self.config.sections():
            data_store = self.config.get(name, 'data_store')
            if data_store == 'psql':
                self.connectors.append(PSQLConnector(name))
            elif data_store == 'mysql':
                self.connectors.append(MySQLConnector(name))
            else:
                print >> sys.stderr, "Skipping section {name} of non-supported data_store {data_store}".format(**locals())

class PSQLConnector(object):
    def __init__(self, name):
        self.name = name

class MySQLConnector(object):
    def __init__(self, name):
        self.name = name
