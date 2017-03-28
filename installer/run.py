import os
import sys
import csv
from installer.tool_config import *
from lib.database import Document, Database
from lib.solr import solr

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
    
    
    # meta to database
    doc = Document()
    doc.clear()
    with open(meta_data_file) as metadata:
        reader = csv.reader(metadata)
        for row in reader:
            doc.create(row[0], row[1])
    doc.close()

    # database to solr
    s = solr()
    db = Database()
    db.connect()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM documents")
    datalist = []
    for row in cursor.fetchall():
        datalist.append({
            "title_s": row["title"],
            "all_txt_ng": row["keywords"],
        })
    cursor.close()
    db.close()
    s.delete(q="*:*")
    s.add(datalist)

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
