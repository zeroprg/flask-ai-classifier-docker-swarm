import cv2
import base64
import time
import sqlite3
import sqlalchemy as sql
from sqlalchemy import text
import psycopg2

class Sql:
    def __init__ (self, DB_USERNAME=None, DB_PASSWORD=None, DATABASE_URI=None, DB_PORT=None, DB_NAME=None):
        """ create a database connection to the SQLite database
            specified by the db_file
        :param db_file: database file
        :return: Connection object or None
        """
        
        self.engine = None
        metadata = sql.MetaData()
        
        if(  DATABASE_URI is None or DATABASE_URI == ''):
            self.engine = sql.create_engine('sqlite://frame.db')
            conn = engine.connect()
            conn.execute("PRAGMA journal_mode=WAL")
            
        else:
            self.engine = sql.create_engine('postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format(DB_USERNAME, DB_PASSWORD, DATABASE_URI, DB_PORT, DB_NAME))

        self.objects = sql.Table('objects', metadata, autoload=True, autoload_with=self.engine)
        self.statistic = sql.Table('statistic', metadata, autoload=True, autoload_with=self.engine)
        ##self.getConn().autocommit = False

    def __init__ (self, SQLALCHEMY_DATABASE_URI):
        """ create a database connection to the SQLite database
            specified by the db_file
        :param db_file: database file
        :return: Connection object or None
        """
        self.engine = None
        metadata = sql.MetaData()

        if(  SQLALCHEMY_DATABASE_URI is None or SQLALCHEMY_DATABASE_URI == ''):
            self.engine = sql.create_engine('sqlite://frame.db')
            conn = engine.connect()
            conn.execute("PRAGMA journal_mode=WAL")
            
        else:
            
            self.engine = sql.create_engine(SQLALCHEMY_DATABASE_URI)

        self.objects = sql.Table('objects', metadata, autoload=True, autoload_with=self.engine)
        self.statistic = sql.Table('statistic', metadata, autoload=True, autoload_with=self.engine)


        #conn = self.engine.connect()
        ##self.getConn().autocommit = False
    
    def getConn(self):
        return self.engine.connect()

 
    def select_all_objects(self):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        #cur = conn.cursor()
        #cur.execute("SELECT hashcode, currentdate, currentime, type, x_dim, y_dim FROM objects  ORDER BY currentime DESC ")
        query = sql.select([self.objects]).limit(50).all()
        ResultProxy = self.getConn().execute(query)
        rows = ResultProxy.fetchall()
        #for row in rows:
        #    print(row)
        return rows

    def insert_statistic(self, params):
        for param in params:
            hashcodes = ''
            length = len(param['hashcodes'])
        # for i in range(length): hashcodes += str(param['hashcodes'][i]) + ',' if i < length - 1 else str(param['hashcodes'][i])
            hashcodes = str(param['hashcodes'])
        if param['y'] == 0: return # never store dummy noise
        try:
            #cur.execute("INSERT INTO statistic(type,currentime,y,text,hashcodes,cam) VALUES ("+self.P+", "+self.P+", "+self.P+", "+self.P+", "+self.P+", "+self.P+")",
            #     (param['name'], param['x'],  param['text'], hashcodes, param['cam']))
            values = {'type': param['name'], 'currentime': param['x'], 'y': param['y'], 'hashcodes': hashcodes, 'cam':param['cam'] }     
            query = sql.insert(self.statistic)
            ResultProxy = self.getConn().execute(query, values)
            print(" insert_statistic was {0} with params: {1}".format(ResultProxy.is_insert ,params))    
        except Exception as e:
            print(" e: {}".format( e))
        

    def select_statistic_by_time(self, cam, time1, time2, obj):
        """
        Query statistic by time
        :param conn: the Connection object
        :param time1, time2 in second INTEGER
        :return:
        """
        now = time.time()
        time2 = int((now - time2*3600000)*1000)
        time1 = int((now - time1*3600000)*1000)
        if time2 > time1:  # swap them 
            a=time2
            time2=time1 
            time1=a

        print(time2,time1, obj)
        tuple_ =  obj.split(',')
        #print(str)
        #cur.execute("SELECT type, currentime as x0, currentime + 30000 as x, y as y FROM statistic WHERE type IN" +str+ " AND cam="+self.P+" AND currentime BETWEEN "+self.P+" and "+self.P+" ORDER BY type,currentime ASC", #DeSC
        #    (cam, time2, time1 ))

        query = sql.select([self.statistic]).where(sql.and_(self.statistic.columns.cam == cam, 
                                                              self.statistic.columns.type.in_(tuple_),
                                                              self.statistic.columns.currentime.between(time2, time1)
                                                             )
                                                    ).order_by(text("currentime asc"))                                                                                         
        ResultProxy = self.getConn().execute(query)
        cursor = ResultProxy.fetchall()    

        # convert row object to the dictionary
        #cursor = cur.fetchall()
        _type = ""
        rows=[]
        for record in cursor:
                type = record[0]
                if(type != _type): 
                    rows.append({'label':record[0],'values': 
                    [ {'x0':v[1], 'x':v[1] + 30000,'y':v[2]} for v in list(filter( lambda x : x[0] == type , cursor))] })
                _type=type
        #print(rows)
        return rows


    def insert_frame(self, hashcode, date, time, type, numpy_array, x_dim, y_dim, cam):
        
         if y_dim <25 or x_dim <25 or x_dim/y_dim > 4.7 or y_dim/x_dim > 4.7: return

        #cur.execute("UPDATE objects SET currentime="+self.P+" WHERE hashcode="+self.P, (time, str(hashcode)))
        print("cam= {}, x_dim={}, y_dim={}".format(cam, x_dim, y_dim))
        buffer = cv2.imencode('.jpg', numpy_array)[1]
        jpg_as_base64='data:image/jpeg;base64,'+ base64.b64encode(buffer).decode('utf-8')


        
        try:
            #cur.execute("INSERT INTO objects (hashcode, currentdate, currentime, type, frame, x_dim, y_dim, cam) VALUES ("+self.P+", "+self.P+", "+self.P+", "+self.P+", "+self.P+", "+self.P+", "+self.P+", "+self.P+")", 
            #(str(hashcode), date, time, type, str(jpg_as_base64), int(x_dim), int(y_dim), int(cam)))
            values = {'hashcode': hashcode, 'currentdate': date, 'currentime': time, 'type': type, 'frame':str(jpg_as_base64), 'x_dim': int(x_dim), 'y_dim': int(y_dim), 'cam':int(cam) }     
            query = sql.insert(self.objects)
            ResultProxy = self.getConn().execute(query, values)
            print(" insert_frame was {0} with params: {1}".format(ResultProxy.is_insert ,values))
        except Exception as e: print(" e: {}".format( e))


    def select_frame_by_time(self, cam, time1, time2):
        """
        Query frames by time
        :param conn: the Connection object
        :param cam, time1, time2 in epoch seconds
        :return:
        """    
        #cur.execute("SELECT cam, hashcode, currentdate, currentime, type, frame FROM objects WHERE cam="+self.P+" AND currentime BETWEEN "+self.P+" and "+self.P+" ORDER BY currentime DESC", (cam,time1,time2,))
        
        query = sql.select([self.objects]).where(sql.and_(self.objects.columns.cam == cam, 
                                                              self.objects.columns.currentime.between(time1, time2)
                                                             )
                                                ).order_by(text("currentime desc"))
                                                                                    
        ResultProxy = self.getConn().execute(query)
        cursor = ResultProxy.fetchall()
        rows = [dict(r) for r in cursor] 
#        rows = [ {'cam':v['çam'] , 'hashcode':v['hashcode'],  'currentdate':v['currentdate'], 'currentime':v['currentime'], 'type': v['type'], 'frame': v['frame'], 'lastdate': v['lastdate'], 'lasttime': v['lasttime']  } for v in ResultProxy ]

        return rows

    def select_last_frames(self, cam, time1, time2, obj,  offset=0, n_rows=50):
        """
        Query last n rows of frames b
        :param conn: the Connection object
        :param n_rows number of rows restrict value of request
        :return:
        """
        now = time.time()
        time2 = int((now - time2*3600000)*1000)
        time1 = int((now - time1*3600000)*1000)
        if time2 > time1:  # swap them 
            a=time2
            time2=time1 
            time1=a
        #str =  "('" + obj.replace(",","','") + "')"    
        print(time2,time1, obj)
        tuple_ =  obj.split(',')
        
        #cur.execute("SELECT cam, hashcode, currentdate, currentime, type, frame FROM objects where cam="+self.P+" AND  type IN " +str+ " AND currentime BETWEEN "+self.P+" and "+self.P+" ORDER BY currentime DESC LIMIT "+self.P+" OFFSET "+self.P+"", 
        #    (cam, time2, time1,n_rows,offset,))
        #fetched_rows = cur.fetchall()
        query = sql.select([self.objects]).where(sql.and_(self.objects.columns.cam == cam, 
                                                              self.objects.columns.type.in_(tuple_),
                                                              self.objects.columns.currentime.between(time2, time1)
                                                         )
                                                ).order_by(text("currentime desc")).limit(n_rows).offset(offset)
                                     
        ResultProxy = self.getConn().execute(query)
        cursor = ResultProxy.fetchall()
        rows = [dict(r) for r in cursor] 

        #cursor = ResultProxy.fetchall()
        #rows = [ {'cam':v['çam'] , 'hashcode':v['hashcode'],  'currentdate':v['currentdate'], 'currentime':v['currentime'], 'type': v['type'], 'frame': v['frame'], 'lastdate': v['lastdate'], 'lasttime': v['lasttime']  } for v in cursor ]
        #print(rows[0])
        return rows



    def delete_frames_later_then(self, hours):
        """
        Delete all records from objects table which are later then 'hours' back
        """
        # predicate : '-70 minutes' , '-1 seconds ', '-2 hour'
        #cur.execute("DELETE from objects WHERE currentime < strftime('"+self.P+"','now'," + predicate+ ")")

        millis_back = int(round(time.time() * 1000)) - hours*60*60*1000
        try:
            query = sql.delete(self.objects).where( self.objects.currentime < millis_back )
            ResultProxy = self.getConn().execute(query)
            print(" delete_frames_later_then was {0} with params: {1}".format(ResultProxy.is_insert ,hours))
        except Exception as e: print(" e: {}".format( e))
    
def main():
    database = "framedata.db"

    # create a database connection
    sql = Sql(database)
    conn = sql.getConn()
    with conn:
        print("1. Query objects by time:")
        sql.select_frame_by_time("2019-01-01 00:00:00.00.000", "2019-12-31 00:00:00.00.000")

        print("2. Query all objects")
        sql.select_all_stats()
 
 
if __name__ == '__main__':
    main()
