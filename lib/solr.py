import pysolr
from config.config import *

class Solr:
    SOLR = pysolr.Solr("http://{host}:{port}/solr/{core}".format(**CONFIG["SOLR"]), timeout=10)

    def solr(self):
        return self.SOLR

    def search(self, q, path = None):
        queries = []
        if q:
            queries.append("all_txt_ng:%s" % self.sanitize(q))
        if path:
            queries.append("path_s:%s*" % self.sanitize(path))
        if not queries:
            return self._empty_res()

        res = self.SOLR.search(" AND ".join(queries))
        return self._prepare_res(res)

    def list(self):
        return self._prepare_res(self.SOLR.search("*:*"))

    def _empty_res(self):
        return {
            "hits": 0,
            "docs": [],
        }

    def _prepare_res(self, res):
        docs = [{"title": d["title_s"], "path": d.get("path_s"), "universal_id": d["universal_id_s"]} for d in res.docs]
        return {
            "hits": res.hits,
            "docs": docs,
        }

    @classmethod
    def sanitize(cls, query):
        if not query:
            return ""
        escapeRules = {'+': r'\+', '-': r'\-', '&': r'\&', '|': r'\|', '!': r'\!',
                   '(': r'\(', ')': r'\)', '{': r'\{', '}': r'\}', '[': r'\[', ']': r'\]', '^': r'\^', '~': r'\~', '*': r'\*', '?': r'\?', ':': r'\:', '"': r'\"', ';': r'\;', ' ': r'\ ', '/': r'\/', 'AND': r'\AND', 'OR': r'\OR', 'NOT': r'\NOT'}
        query = query.replace('\\', r'\\')
        for k, v in escapeRules.items():
            query = query.replace(k, v)
        return query

