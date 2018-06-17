#!/usr/bin/python
# -*- coding: utf-8 -*-

from psycopg2 import connect
import sys
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

argvs = sys.argv  
argc = len(argvs) 

dbname = argvs[1]

con = None
con = connect(dbname='postgres', user='postgres', host = 'localhost', password='')

con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = con.cursor()
cur.execute('DROP DATABASE ' + dbname)
cur.close()
con.close()
