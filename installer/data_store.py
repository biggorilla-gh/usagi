import psycopg2

class PSQLHandle(object):
    def __init__(self, name, dsn):
        self.SQL_GET_META_DATA = """
SELECT
    CASE WHEN schema_name = 'public' THEN table_name
        ELSE schema_name || '.' || table_name END AS title,
    schema_name || ' '
    || table_name || ' '
    || table_comment || ' '
    || string_agg(column_name || ' ' || column_comment, ' ') AS content
FROM
(
SELECT
  psut.relid table_oid,
    psut.schemaname schema_name,
    psut.relname table_name,
    CASE WHEN pd.description IS NULL THEN '' ELSE pd.description END table_comment
FROM
    pg_stat_user_tables psut
LEFT JOIN
(
    SELECT *
    FROM
        pg_description pd
    WHERE
        pd.objsubid IS NULL OR pd.objsubid = 0
) pd
ON
    psut.relid = pd.objoid
) r
JOIN
(
SELECT
  psut.relid table_oid,
    pa.attname column_name,
    CASE WHEN pd.description IS NULL THEN '' ELSE pd.description END column_comment
FROM
    pg_stat_user_tables psut
JOIN
    pg_attribute pa
ON
    psut.relid = pa.attrelid
LEFT JOIN
(
    SELECT *
    FROM
        pg_description pd
    WHERE
        pd.objsubid IS NULL OR pd.objsubid != 0
) pd
ON
    psut.relid = pd.objoid AND pd.objsubid = pa.attnum
) s
USING (table_oid)
GROUP BY schema_name, table_name, table_comment"""

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

