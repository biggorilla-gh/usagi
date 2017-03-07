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
                if self.config.has_option(name, 'port'):
                    try:
                        self.config.getint(name, 'port')
                    except ValueError:
                        print >> sys.stderr, \
                                """Unexpected value of "port" found in section [{name}].
                                """.format(**locals())
                        return False
                dsn = " ".join([k+"="+v for k, v in self.config.items(name)])
                self.handles.append(PSQLHandle(name, dsn))
            elif data_store == 'mysql':
                params = {}
                for k, v in self.config.items(name):
                    try:
                        if k in ('port', 'connect_timeout'):
                            params[k] = self.config.getint(name, k)
                        elif k == 'compress':
                            params[k] = self.config.getboolean(name, k)
                        else:
                            params[k] = v
                    except ValueError:
                        print >> sys.stderr, \
                                """Unexpected value of "{k}" found in section [{name}].
                                """.format(**locals())
                        return False
                self.handles.append(MySQLHandle(name, params))
            else:
                print >> sys.stderr, \
                        """Found section [{name}] of non-supported data_store "{data_store}".
                        (psql, mysql) are currently supported.
                        """.format(**locals())
                return False
        return True

