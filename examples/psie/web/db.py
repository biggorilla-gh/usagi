import psycopg2
import psycopg2.extras
import pysolr


def database():
    connect = psycopg2.connect(
        "dbname=psie host=localhost port=5432 user=psie password=psie")
    cur = connect.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return cur


def solr():
    return pysolr.Solr("http://localhost:8983/solr/psie", timeout=10)


def solr_sanitize(query):
    if not query:
        return ""
    escapeRules = {'+': r'\+', '-': r'\-', '&': r'\&', '|': r'\|', '!': r'\!',
                   '(': r'\(', ')': r'\)', '{': r'\{', '}': r'\}', '[': r'\[', ']': r'\]', '^': r'\^', '~': r'\~', '*': r'\*', '?': r'\?', ':': r'\:', '"': r'\"', ';': r'\;', ' ': r'\ ', '/': r'\/', 'AND': r'\AND', 'OR': r'\OR', 'NOT': r'\NOT'}
    query = query.replace('\\', r'\\')
    for k, v in escapeRules.items():
        query = query.replace(k, v)
    return query
