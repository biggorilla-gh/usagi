from __future__ import print_function
import sys
import configparser

class SearchConfiguration(object):
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        self.handles = []

    def get_search_config(self):
        self.config = configparser.SafeConfigParser()
        self.config.read(self.config_file_path)

    def parse(self):
        for name in self.config.sections():
            conf = dict(self.config.items(name))
            data_store = conf['data_store'] if 'data_store' in conf else ''
            try:
                if data_store == 'psql':
                    from installer.data_store.psql_handle import PSQLHandle
                    self.handles.append(PSQLHandle(name, conf))
                elif data_store == 'mysql':
                    from installer.data_store.mysql_handle import MySQLHandle
                    self.handles.append(MySQLHandle(name, conf))
                elif data_store == 'meta':
                    from installer.data_store.meta_handle import MetaHandle
                    self.handles.append(MetaHandle(name, conf))
                else:
                    raise Exception("""Found section [{name}] of non-supported data_store "{data_store}".
                        (psql, mysql, meta) are currently supported.
                        """.format(**locals()))
            except Exception as e:
                print(sys.exc_info()[1], file=sys.stderr)
                return False
        return True

