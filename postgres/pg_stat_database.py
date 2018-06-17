import time
import psycopg2
import os

connection3 = psycopg2.connect(host="127.0.0.1", port=5432, database="sample", user="postgres", password="")
cursor5 = connection3.cursor()
cursor5.execute("SELECT * FROM pg_stat_database WHERE datname = 'sample';")
stats = cursor5.fetchall()

#  datid |  datname   | numbackends | xact_commit | xact_rollback | blks_read  |  blks_hit   | tup_returned | tup_fetched | tup_inserted | tup_updated | tup_deleted | conflicts | temp_files |  temp_bytes  | deadlocks | blk_read_time | blk_write_time |          stats_reset          |     size

result = {}
for stat in stats:
    database = stat[1]
    result[database] = stat

#print stats

print "datid |  datname   | numbackends | xact_commit | xact_rollback | blks_read  |  blks_hit   | tup_returned | tup_fetched | tup_inserted | tup_updated | tup_deleted | conflicts | temp_files |  temp_bytes  | deadlocks | blk_read_time | blk_write_time | stats_reset | size"

#print stats

for database in result:
    for i in range(2,len(cursor5.description)):
        metric = cursor5.description[i].name
        value = result[database][i]
        try:
            if metric in ("stats_reset"):
                continue
            print ("postgresql.%s %i %s database=%s"
                   % (metric, ts, value, database))
        except:
            #utils.err("got here")
            continue

#print "datid |  datname   | numbackends | xact_commit | xact_rollback | blks_read  |  blks_hit   | tup_returned | tup_fetched | tup_inserted | tup_updated | tup_deleted | conflicts | temp_files |  temp_bytes  | deadlocks | blk_read_time | blk_write_time | stats_reset | size"
        
for row in stats:
    print "---"
    print "dataid -- " + unicode(row[0])
    print "datname -- " + unicode(row[1])
    print "numbackends -- " + unicode(row[2])
    print "xact_commit -- " + unicode(row[3])
    print "blks_read -- " + unicode(row[4])
    print "blks_hit -- " + unicode(row[5])

    print "tup_returned -- " +unicode(row[6])
    print "tup_fetched -- " + unicode(row[7])
    print "tup_inserted -- " +unicode(row[8])
    print "tup_updated -- " + unicode(row[9])
    print "tup_deleted -- " + unicode(row[10])
    print "conflicts -- " + unicode(row[11])

    print "temp_files -- " + unicode(row[12])
    print "temp_bytes -- " + unicode(row[13])
    print "deadlocks -- " + unicode(row[14])
    print "blk_read_time -- " + unicode(row[15])
    print "blk_write_time -- " + unicode(row[16])
    print "starts_reset -- " + unicode(row[17])
    print "size -- " + unicode(row[18])
