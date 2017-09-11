import os
import csv

class MetaHandle(object):
    def __init__(self, name, conf):
        self.name = name
        self.path = conf['path']

    def copy_raw_meta_data(self, output_filepath, append=False):
        with open(self.path) as i:
           with open(output_filepath, 'a' if append else 'w') as o:
                reader = csv.reader(i)
                writer = csv.writer(o)
                for row in reader:
                    title = row.pop(0)
                    uid = "{}.{}".format(self.name, title)
                    r = [uid, title]
                    for v in row:
                        r.append(v)
                    writer.writerow(r)

