import pysolr
from config.config import *

def solr():
    return pysolr.Solr("http://{host}:{port}/solr/{core}".format(**CONFIG["SOLR"]), timeout=10)

def solr_sanitize(query):
    if not query:
        return ""
    escapeRules = {'+': r'\+', '-': r'\-', '&': r'\&', '|': r'\|', '!': r'\!',
                   '(': r'\(', ')': r'\)', '{': r'\{', '}': r'\}', '[': r'\[', ']': r'\]', '^': r'\^', '~': r'\~', '*': r'\*', '?': r'\?', ':': r'\:', '"': r'\"', ';': r'\;', ' ': r'\ ', '/': r'\/', 'AND': r'\AND', 'OR': r'\OR', 'NOT': r'\NOT'}
    query = query.replace('\\', r'\\')
    for k, v in escapeRules.items():
        query = query.replace(k, v)
    return query
