import MySQLdb
from MySQLdb.cursors import DictCursor

print("Database Host: (localhost) ", end="")
host = input()
host = host if host else 'localhost'
print("Database User: (root) ", end="")
user = input()
user = user if user else 'root'
print("Database Password: ", end=""),
password = input()
print("Database Name: ", end=""),
name = input()
connect = MySQLdb.connect(db=name, host=host, port=3306, user=user, passwd=password)
cur = connect.cursor(DictCursor)

cur.execute("show tables")
for table in cur.fetchall():
    table_name = table["Tables_in_{}".format(name)]
    print(table_name)
    cur.execute("describe {}".format(table_name))
    print(cur.fetchall())

# dependencies
cur.execute("""
select
  k.constraint_name as name,
  k.table_name as src_table,
  k.referenced_table_name as dest_table,
  k.column_name as src_column,
  k.referenced_column_name as dest_column
from
information_schema.key_column_usage k
left join information_schema.table_constraints c
  on k.table_schema = c.table_schema
  and k.constraint_name = c.constraint_name
  where c.constraint_type = 'FOREIGN KEY'
  and k.table_schema = %s
""", (name,))
for dep in cur.fetchall():
    print(dep)
