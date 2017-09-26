import pycountry
import os

for c in pycountry.countries:
    code = c.alpha_3
    os.system("curl 'http://data.biogeo.ucdavis.edu/data/gadm2.8/shp/{}_adm_shp.zip' -o zip/{}.zip".format(code, code))
