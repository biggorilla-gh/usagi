
class GeoMap:
    def __init__(self, filename):
        self.data = []
        f = open(filename)
        for row in f:
            s = row.split("\t")
            if len(s) != 3:
                continue
            self.data.append({
                "level": int(s[0]),
                "name": s[1],
                "namel": s[1].lower(),
                "loc": list(map(float, s[2].split(","))),
            })
        f.close()

    def findByName(self, keyword, maxSize = 10):
        kw = [v.lower() for v in keyword.split()]
        matches = []
        for d in self.data:
            nf = False
            for k in kw:
                if d["namel"].find(k) == -1:
                    nf = True
                    break
            if not nf:
                d["score"] = 1000 - len(d["name"])
                matches.append(d)
        matches = sorted(matches, key=lambda x: -x["score"])
        return matches[:20]

    def findByLocation(self, loc, maxSize = 10):
        matches = []
        nloc = [
            loc[0] if loc[0] > 0 else loc[0] + 360,
            loc[1] if loc[1] > 0 else loc[1] + 180,
        ]
        for d in self.data:
            l = d["loc"]
            nl = [
                l[0] if l[0] > 0 else l[0] + 360,
                l[1] if l[1] > 0 else l[1] + 180,
                l[2] if l[2] > 0 else l[2] + 360,
                l[3] if l[3] > 0 else l[3] + 180,
            ]
            if nl[0] > nloc[0]:
                continue
            if nl[2] < nloc[0]:
                continue
            if nl[1] > nloc[1]:
                continue
            if nl[3] < nloc[1]:
                continue
            matches.append(d)
            if len(matches) > maxSize:
                break
        return matches
