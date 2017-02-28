import os
import sys
from installer.tool_config import *

def main(args):
    if len(args) != 2:
        pass
    else:
        ds_config, meta_data_file = args

    if not os.path.exists(ds_config):
        print >> sys.stderr, "%s does not exists" % ds_config
        return 1

    if os.path.exists(meta_data_file):
        print >> sys.stderr, "%s already exists, please remove it first" % meta_data_file
        return 1

    if not os.path.exists(os.path.dirname(meta_data_file)):
        print >> sys.stderr, "dir %s does not exists, please create it first" % os.path.dirname(meta_data_file)
        return 1

    sc = SearchConfiguration(ds_config)
    sc.get_search_config()
    sc.parse()

    for handle in sc.handles:
        handle.connect()
        handle.copy_raw_meta_data(meta_data_file, append=True)
        handle.close()

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
