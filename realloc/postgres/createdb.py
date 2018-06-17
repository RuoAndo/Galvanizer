#!/usr/bin/python
# -*- coding: utf-8 -*-

from psycopg2 import connect
import sys
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

argvs = sys.argv  
argc = len(argvs) 

dbname = "realloc"
dbname2 = "realloc_2"

con = None
con = connect(dbname='postgres', user='postgres', host = 'localhost', password='')

con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = con.cursor()

try:
    cur.execute('CREATE DATABASE ' + dbname)
except:
    print "dbname error"
    pass

try:
    cur.execute('CREATE DATABASE ' + dbname2)
except:
    print "dbname2 error"
    pass
    
cur.close()
con.close()
