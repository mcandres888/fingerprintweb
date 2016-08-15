from library import *
import binascii
import time
import datetime
import sqlite3 as lite
import time

class SQLDatabase:
    def __init__ (self, dbfile ):
        self.dbfile = dbfile
        self.init_db_struct()

    def close(self):
        self.con.close()


    def reconnect(self):
        try:
            self.con = lite.connect(self.dbfile)
            self.cur = self.con.cursor()
            return self.con
        except lite.Error, e:
            sys.exit(1)

    def exec_query ( self, query_str ):
        self.reconnect()
        self.cur.execute(query_str)
        self.con.commit()
        self.close()

    def isIdExists ( self, id , table ) :
        self.reconnect()
        query_str = "SELECT * from %s WHERE Id=%d" % (table, id)
        self.cur.execute(query_str)
        row = self.cur.fetchone()
        if row == None:
            row = []
        self.close()
        return row

    def getAll ( self, table, sort=0 ):
        if sort == 1:
            query_str = "SELECT * FROM %s ORDER BY id DESC" % table
        else:
            query_str = "SELECT * FROM %s" % table
        print query_str
        self.reconnect()
        self.cur.execute(query_str)
        rows = self.cur.fetchall()
        if rows == None:
            rows = []
        self.close()
        return rows

#######################################################
#
#   D A T A B A S E   I N I T I A L I Z A T I O N
#
#######################################################


    def init_db_struct(self):
        self.init_fdata()
        self.populate_fdata ()
        self.init_images ()
        self.init_activity ()

    def init_fdata (self):
        self.reconnect()
        self.cur.execute("CREATE TABLE if not exists  FDATA (id INT,name TEXT,status INT)")
        self.con.commit()
        self.close()

    def init_activity (self):
        self.reconnect()
        self.cur.execute("CREATE TABLE if not exists  ACTIVITY (id INT,type TEXT,note TEXT)")
        self.con.commit()
        self.close()



    def init_images (self):
        self.reconnect()
        self.cur.execute("CREATE TABLE if not exists IMAGES (id INT,path TEXT)")
        self.con.commit()
        self.close()


    def populate_fdata (self):
        # populate with initial values
        # we set it only to 10 fingerprints even though it can 
        # save many of them
        for  x in range (1, 11):
            if len(self.isIdExists(x, 'FDATA')) > 0 :
                print "id exists"
                continue
            query_str = "INSERT INTO FDATA VALUES('%d', 'empty', 0)" % x
            print query_str
            self.exec_query(query_str)


#######################################################
#
#   D A T A B A S E   F U N C T I O N S
#
#######################################################

    def formatFDATA ( self, data ):
        temp = {}
        temp['id'] = data[0]
        temp['name'] = data[1]
        temp['status'] = data[2]
        return temp
    
    def getAllFDATA (self):
        rows = self.getAll("FDATA" )
        data = []
        for x in rows:
            data.append(self.formatFDATA(x))
        return data

    def updateFDATA ( self, id, name):
        query_str = "UPDATE FDATA SET name='%s' WHERE id=%d" % (name, int(id))
        self.exec_query (query_str)



    def formatActivity ( self, data ):
        temp = {}
        temp['id'] = data[0]
        temp['type'] = data[1]
        temp['note'] = data[2]
        temp['time'] = str(datetime.datetime.fromtimestamp(data[0]).strftime('%c'))
        return temp

 
    def getAllActivities (self):
        rows = self.getAll("ACTIVITY", 1 )
        data = []
        for x in rows:
            data.append(self.formatActivity(x))
        return data

    def insertActivity ( self, type, note):
        # get time now
        epoch_time = int(time.time())
        query_str = "INSERT INTO ACTIVITY VALUES (%d ,'%s', '%s')" % (epoch_time, type, note)
        self.exec_query (query_str)

    def insertImage ( self, path):
        # get time now
        epoch_time = int(time.time())
        query_str = "INSERT INTO IMAGES VALUES (%d, '%s')" % (epoch_time, path)
        self.exec_query (query_str)

    def formatImages ( self, data ):
        temp = {}
        temp['id'] = data[0]
        temp['path'] = data[1]
        temp['time'] = str(datetime.datetime.fromtimestamp(data[0]).strftime('%c'))
        return temp

    def getAllImages (self):
        rows = self.getAll("IMAGES", 1 )
        data = []
        for x in rows:
            data.append(self.formatImages(x))
        return data




