import psycopg2

class PSQLHandle(object):
    def __init__(self, name, dsn):
        self.SQL_GET_META_DATA = """
SELECT
    t.table_schema,
    t.table_name,
    jsonb_object_agg(c.column_name, c.data_type) AS col_to_type
FROM
    information_schema.tables t,
    information_schema.columns c
WHERE
    t.table_schema != 'information_schema'
AND t.table_schema != 'pg_catalog'
AND t.table_schema = c.table_schema
AND t.table_name = c.table_name
GROUP BY
    t.table_schema, t.table_name"""

        self.name = name
        self.dsn = dsn

    def connect(self):
        self.connection = psycopg2.connect(self.dsn)

    def close(self):
        self.connection.close()

    def copy_raw_meta_data(self, output_path):
        cur = self.connection.cursor()
        f = open(output_path, 'w')
        sql_copy = "COPY (%s) TO STDOUT WITH CSV HEADER" % self.SQL_GET_META_DATA
        cur.copy_expert(sql_copy, f)
        f.close()
        cur.close()


class MySQLHandle(object):
    def __init__(self, name):
        self.name = name

