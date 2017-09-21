import csv
import MySQLdb

class MySQLHandle(object):
    SQL_GET_META_DATA = """
SELECT
    concat('{section}', ".", t.table_schema, ".", t.table_name) as universal_id,
    concat(t.table_schema, '.', t.table_name) AS title,
    concat_ws(' ', t.table_schema, t.table_name, t.table_comment,
        group_concat(
            concat(c.column_name, ' ', c.column_comment) SEPARATOR ' '
        )
    ) AS content,
    concat('{section}', '/', t.table_schema) as path
FROM
    information_schema.tables t,
    information_schema.columns c
WHERE
    t.table_schema NOT IN
    (
        'performance_schema',
        'mysql',
        'sys',
        'information_schema'
    )
AND t.table_name = c.table_name
AND t.table_schema IN {databases}
GROUP BY
    t.table_schema, t.table_name, t.table_comment"""

    def __init__(self, name, conf):
        self.name = name
        del conf['data_store']
        params = {}
        for k, v in conf.items():
            try:
                if k in ('port', 'connect_timeout'):
                    params[k] = int(v)
                elif k == 'compress':
                    params[k] = bool(v)
                else:
                    params[k] = v
            except ValueError:
                raise Exception("""Unexpected value of "{}" found in section [{}].
                    """.format(k, name))
        self.databases = [d.strip() for d in params.pop('db').split(',')]
        self.params = params

    def connect(self):
        self.connection = MySQLdb.connect(**self.params)

    def close(self):
        self.connection.close()

    def copy_raw_meta_data(self, output_path, append=False):
        cur = self.connection.cursor()
        f = open(output_path, 'a' if append else 'w')
        cur.execute(MySQLHandle.SQL_GET_META_DATA.format(
            section=self.name,
            databases=str(tuple(self.databases)).replace('u', '')
        ))
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(list(cur))
        f.close()
        cur.close()

