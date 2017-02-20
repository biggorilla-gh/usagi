import sys
import ConfigParser
from installer.data_store import *

class SearchConfiguration(object):
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        self.handles = []

    def get_search_config(self):
        self.config = ConfigParser.SafeConfigParser()
        self.config.read(self.config_file_path)

    def parse(self):
        for name in self.config.sections():
            data_store = self.config.get(name, 'data_store')
            self.config.remove_option(name, 'data_store')

            if data_store == 'psql':
                dsn = " ".join([k+"="+v for k, v in self.config.items(name)])
                self.handles.append(PSQLHandle(name, dsn))
            elif data_store == 'mysql':
                self.handles.append(MySQLHandle(name))
            else:
                print >> sys.stderr, "Skipping section {name} of non-supported data_store {data_store}".format(**locals())

