import os
import datetime
import time

import MyBruGISDeployConf as MDC
import MyBruGISDeployLibrary as MDL
from printAndLog import printAndLog
import sendmail
import sys
import psycopg2

migrationTo = "sta"

def clean_gwc_db(host,user):
    try:
        print("Start reset gwc db process")
        print("Get local IP")
        the_ip = MDL.getIP()
        print(the_ip)
        last_part = the_ip.split('.')[3]
        db_name = "gs_gwc_tiles_%s" % (last_part)
        conn_s = "dbname='%s' user='%s' host='%s' password='%s'" % (db_name, user,host, user)
        print(conn_s)
        with psycopg2.connect(conn_s) as conn:
            cur = conn.cursor()
            cur.execute("""TRUNCATE tilepage CASCADE;""")
        '''old_isolation_level = conn.isolation_level
        conn.set_isolation_level(0)
        cur.execute("""VACUUM FULL""")
        conn.set_isolation_level(old_isolation_level)'''
        print("SUCCEED")
        return True
    except:
        print("FAILED", sys.exc_info())
        return False

clean_gwc_db(MDC.gwcJdbcConfig[migrationTo]["DBHOST"],"gsgwctiles")