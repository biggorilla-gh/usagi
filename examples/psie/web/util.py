from collections import OrderedDict
import json

def geojson_dumps(j):
    return json.dumps(OrderedDict([
        ('type', j['type']),
        ('coordinates', j['coordinates']),
    ]))

def normalize_polygon_coordinates(coordinates):
    normalized = []
    for c in coordinates:
        ccc = [normalize(cc) for cc in c]
        normalized.append(ccc)
    return normalized

def normalize(cc):
    n = False
    if cc[0] > 180:
        cc[0] -= 360
        n = True
    if cc[0] < -180:
        cc[0] += 360
        n = True
    if cc[1] > 90:
        cc[1] -= 180
        n = True
    if cc[1] < -90:
        cc[1] += 180
        n = True
    if n:
        return normalize(cc)
    return cc
