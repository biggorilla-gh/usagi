import pycountry
import shapefile
import os

def find_shapefile(cn):
    os.system("rm -rf zip/{} > /dev/null".format(cn))
    os.system("unzip zip/{}.zip -d zip/{} > /dev/null".format(cn, cn))
    files = []
    for i in [0,1,2,3,4,5,6,7,8]:
        name = "zip/{}/{}_adm{}.shp".format(cn, cn, i)
        if os.path.exists(name):
            files.append(name)
    return files

for c in pycountry.countries:
    files = find_shapefile(c.alpha_3)
    for level, f in enumerate(files):
        sf = shapefile.Reader(f)
        for r, s in zip(sf.records(), sf.shapes()):
            l = []
            for i in range(1, level+2):
                l.append(str(r[i*2]))
            data = [
                str(level),
                " ".join(l).strip().replace("\n", ""),
                ",".join(map(str, s.bbox))
            ]
            print("\t".join(data))
