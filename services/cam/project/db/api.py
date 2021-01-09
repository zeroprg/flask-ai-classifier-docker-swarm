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
        self.limit = 150
        metadata = sql.MetaData()
        if(  DATABASE_URI is None or DATABASE_URI == ''):
            self.engine = sql.create_engine('sqlite://frame.db')
            conn = self.engine.connect()
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
        self.limit = 150
        metadata = sql.MetaData()

        if(  SQLALCHEMY_DATABASE_URI is None or SQLALCHEMY_DATABASE_URI == ''):
            self.engine = sql.create_engine('sqlite://frame.db')
            conn = self.engine.connect()
            conn.execute("PRAGMA journal_mode=WAL")
        else:
            self.engine = sql.create_engine(SQLALCHEMY_DATABASE_URI)

        self.objects = sql.Table('objects', metadata, autoload=True, autoload_with=self.engine)
        self.statistic = sql.Table('statistic', metadata, autoload=True, autoload_with=self.engine)
        self.urls = sql.Table('urls', metadata, autoload=True, autoload_with=self.engine)
        self.obj_stat = sql.Table('obj_stat', metadata, autoload=True, autoload_with=self.engine)


        #conn = self.engine.connect()
        ##self.getConn().autocommit = False

    def getConn(self):
        return self.engine.connect()

# ####################  Obj_stat operations ######################################## #


    def select_all_obj_stat(self):
        """
        Query all rows in the urls table
        :return:
        """
        query = sql.select([self.obj_stat]).limit(self.limit).all()
        ResultProxy = self.getConn().execute(query)
        rows = ResultProxy.fetchall()
        return rows

    def insert_obj_stat(self, params):
        try:
            values = {'cam_uuid': params['cam_uuid'],'type': params['type'], 'last_10min':params['last_10min'], 'last_hour': params['last_hour'], 'last_day': params['last_day'] }
            query = sql.insert(self.obj_stat)
            ResultProxy = self.getConn().execute(query, values)
            print(" insert_obj_stat was {0} with params: {1}".format(ResultProxy.is_insert ,params))
        except Exception as e:
            print(" e: {}".format( e))

# ####################  Urls operations ######################################## #


    def select_all_urls(self):
        """
        Query all rows in the urls table
        :return:
        """
        query = sql.select([self.urls]).order_by(text("cam asc"))
        ResultProxy = self.getConn().execute(query)
        cursor = ResultProxy.fetchall()
        rows = [dict(r) for r in cursor]
        return rows

    def insert_urls(self, params):
        try:
            query = sql.insert(self.urls)
            ResultProxy = self.getConn().execute(query, params)
            row_id = None
            for result in ResultProxy: row  = result
            print(" insert_urls was {0} with params: {1}".format(ResultProxy.is_insert ,params))
        except Exception as e:
            print(" e: {}".format( e))
        return row 

    def update_urls(self, params):
        try:
            if params['id'] is not None:
                query = sql.update(self.urls).filter(self.urls.c.id == params['id']).values(cam=params['cam'], os=params['os'], url=params['url'])
            else:    
                query = sql.update(self.urls).filter(self.urls.c.url == params['url']).values(cam=params['cam'], os=params['os'])
            ResultProxy = self.getConn().execute(query, params)
            print(" update_urls was {0} with params: {1}".format(ResultProxy.is_insert ,params))
        except Exception as e:
            print(" e: {}".format( e))



# ####################  Statistic operations ######################################## #

    def insert_statistic(self, params):
        for param in params:
            hashcodes = ''
            hashcodes = str(param['hashcodes'])
        if param['y'] == 0: return # never store dummy noise
        try:
            values = {'type': param['name'],'currentime': param['x'], 'y': param['y'], 'hashcodes': hashcodes, 'cam':param['cam'] }     
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
        #cur.execute("SELECT type, currentime as x0, currentime + 30000 as x, y as y FROM statistic filter type IN" +str+ " AND cam="+self.P+" AND currentime BETWEEN "+self.P+" and "+self.P+" ORDER BY type,currentime ASC", #DeSC
        #    (cam, time2, time1 ))

        query = sql.select([self.statistic]).filter(sql.and_(self.statistic.columns.cam == cam, 
                                                              self.statistic.columns.type.in_(tuple_),
                                                              self.statistic.columns.currentime.between(time2,time1)
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

# ####################  Objects operations ######################################## #

    def select_all_objects(self):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        query = sql.select([self.objects]).limit(self.limit).all()
        ResultProxy = self.getConn().execute(query)
        cursor = ResultProxy.fetchall()
        rows = [dict(r) for r in cursor]
        return rows


    def insert_frame(self, hashcode, date, time, type, numpy_array, x_dim, y_dim, cam):
        if y_dim <25 or x_dim <25 or x_dim/y_dim > 4.7 or y_dim/x_dim > 4.7: return
        #cur.execute("UPDATE objects SET currentime="+self.P+" filter hashcode="+self.P, (time, str(hashcode)))
        #print("cam= {}, x_dim={}, y_dim={}".format(cam, x_dim, y_dim))
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
        now = time.time()
        time2 = int((now - time2*3600000)*1000)
        time1 = int((now - time1*3600000)*1000)
        if time2 > time1:  # swap them 
            a=time2
            time2=time1 
            time1=a


        #cur.execute("SELECT cam, hashcode, currentdate, currentime, type, frame FROM objects filter cam="+self.P+" AND currentime BETWEEN "+self.P+" and "+self.P+" ORDER BY currentime DESC", (cam,time1,time2,))
        query = sql.select([self.objects]).filter(sql.and_(self.objects.columns.cam == cam,                                                           
                                                              self.objects.columns.currentime.between(time2,time1)
                                                             )
                                                ).order_by(text("currentime desc"))

        ResultProxy = self.getConn().execute(query)
        cursor = ResultProxy.fetchall()
        rows = [dict(r) for r in cursor]

        return rows

    def select_last_frames(self, cam, time1, time2, obj,  offset=0):
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
        
        #cur.execute("SELECT cam, hashcode, currentdate, currentime, type, frame FROM objects filter cam="+self.P+" AND  type IN " +str+ " AND currentime BETWEEN "+self.P+" and "+self.P+" ORDER BY currentime DESC LIMIT "+self.P+" OFFSET "+self.P+"", 
        #    (cam, time2, time1,n_rows,offset,))
        #fetched_rows = cur.fetchall()
        query = sql.select([self.objects]).filter(sql.and_(self.objects.columns.cam == cam, 
                                                              self.objects.columns.type.in_(tuple_),
                                                              self.objects.columns.currentime.between(time2,time1)
                                                         )
                                                ).order_by(text("currentime desc")).limit(self.limit).offset(offset)
        ResultProxy = self.getConn().execute(query)
        cursor = ResultProxy.fetchall()
        rows = [dict(r) for r in cursor]
        return rows



    def delete_frames_later_then(self, hours):
        """
        Delete all records from objects table which are later then 'hours' back
        """
        # predicate : '-70 minutes' , '-1 seconds ', '-2 hour'
        #cur.execute("DELETE from objects filter currentime < strftime('"+self.P+"','now'," + predicate+ ")")

        millis_back = int(round(time.time() * 1000)) - hours*60*60*1000
        try:
            query = sql.delete(self.objects).filter( self.objects.currentime < millis_back )
            ResultProxy = self.getConn().execute(query)
            print(" delete_frames_later_then was {0} with params: {1}".format(ResultProxy.is_insert ,hours))
        except Exception as e: print(" e: {}".format( e))
    
def main():
    database = "framedata.db"

    # create a database connection
    sql = Sql(database)
    conn = sql.getConn() 
 
if __name__ == '__main__':
    main()
