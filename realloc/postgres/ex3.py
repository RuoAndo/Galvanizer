# -*- coding: utf-8 -*- 

import psycopg2
import numpy
import numpy as np

import sys 
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT 

argvs = sys.argv  
argc = len(argvs) 

dbname = argvs[1]
tblname = argvs[2]

con = psycopg2.connect(host="127.0.0.1", database="realloc2", user="postgres", password="")
con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

cur= con.cursor()

#sql = '''CREATE TABLE  IF NOT EXISTS  t01prefecture(pref_cd INTEGER, pref_name TEXT);'''
#cur.execute(sql)

#sqlstr = "CREATE TABLE " + "test2" + "(REALLOC_LINENUMBER INT, FILENAME VARCHAR(50), FUNCTION_LINENUMBER VARCHAR(50));"
#sqlstr = 
#print sqlstr
cur.execute("create table test2(id int);")
con.commit
