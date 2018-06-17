# inserting definitions
# libxl_ctx_free:int libxl_ctx_free(libxl_ctx *ctx):libxl.c:79
# libxl_string_list_destroy:void libxl_string_list_destroy(libxl_string_list *psl):libxl.c:87

import sys 
import psycopg2

conn = psycopg2.connect(
    host = "127.0.0.1",
    port = 5432,
    database="sample",
    user="postgres",
    password="")

cur = conn.cursor()

software_version = "test"
function_name = "test"
location = "test"
linenumber = 0
counter = 10
functype = "test"
listtype = "test"

sql = "INSERT INTO definition (id, software_version, type, function_type, function_name, location, linenumber) VALUES (" + str(counter) + ", '" + software_version + "', '" + listtype + "', '" + functype + "', '" + function_name + "', '" + location + "', '" + str(linenumber) +"');"

print sql

cur.execute(sql)
conn.commit()

cur.close()
conn.close()
