import os

class MetaHandle(object):
    def __init__(self, name, conf):
        self.name = name
        self.path = conf['path']

    def copy_raw_meta_data(self, output_filepath, append=False):
       with open(self.path) as i:
           with open(output_filepath, 'a' if append else 'w') as o:
                o.write(i.read())

