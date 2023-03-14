import cv2
import base64
import time
import logging
import re
import sqlalchemy as sql
from sqlalchemy import text
# import psycopg2

logging.basicConfig(level=logging.INFO)

class Sql:
    def __init__ (self, DB_USERNAME=None, DB_PASSWORD=None, DATABASE_URI=None, DB_PORT=None, DB_NAME=None):
        """ create a database connection to the SQLite database
            specified by the db_file
        :param db_file: database file
        :return: Connection object or None
        """
        self.engine = None
        self.limit = 50
        metadata = sql.MetaData()
        postgres_str= 'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format(DB_USERNAME, DB_PASSWORD, DATABASE_URI, DB_PORT, DB_NAME)
        print("DB Connection uri: {}".format(postgres_str)) 
        self.engine = sql.create_engine(postgres_str, pool_pre_ping=True)

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
        self.limit = 70
        metadata = sql.MetaData()

        self.engine = sql.create_engine(SQLALCHEMY_DATABASE_URI, pool_pre_ping=True )

        self.objects = sql.Table('objects', metadata, autoload=True, autoload_with=self.engine)
        self.statistic = sql.Table('statistic', metadata, autoload=True, autoload_with=self.engine)
        self.urls = sql.Table('urls', metadata, autoload=True, autoload_with=self.engine)


        #conn = self.engine.connect()
        ##self.getConn().autocommit = False

    def getConn(self):
        return self.engine.connect()


# ####################  Service utility operations ######################################## #
    def delete_old_images_older_then(self, DAYS_IN_MILLSEC):
        now = time.time()*1000
        _time = int(now - DAYS_IN_MILLSEC)
        conn = self.getConn()
        try:
            if DAYS_IN_MILLSEC is not None:
                query = sql.delete(self.objects).where(self.objects.c.currentime < _time)
            else:    
                raise Exception('No value defined for parameter DAYS_IN_MILLSEC')
            conn.execute(query)
            logging.debug(" objects were deleted for date later then {} days".format(DAYS_IN_MILLSEC/3600000/24))
        except Exception as e:
            logging.debug(" e: {}".format( e))
        finally:
            conn.close()


# ####################  Urls operations ######################################## #
    def select_urls_by_os(self, os):
        query = sql.select([self.urls]).where(self.urls.c.os == str(os)).order_by(text("currentime asc"))
        conn = self.getConn()
        ResultProxy = conn.execute(query)
        cursor = ResultProxy.fetchall()
        rows = [dict(r) for r in cursor]        
        conn.close()
        return rows

    def update_urls_by_os(self, params):
        _time = int(time.time()*1000)
        params['last_time_updated'] =  _time
        conn = self.getConn()
        try:
            if params['os'] is not None:
                query = sql.update(self.urls).where(self.urls.c.os == str(params['os']))
            else:    
                raise Exception('No value defined for parameter os')
            ResultProxy = conn.execute(query,params)
        except Exception as e:
            logging.debug(" e: {}".format( e))
        else:
            logging.debug(" urls was updated  with params: {}".format(ResultProxy.last_updated_params() ))
        finally:
            conn.close()

    def select_all_urls(self):
        """
        Query all rows in the urls table
        :return:
        """
        conn = self.getConn()
        query = sql.select([self.urls]).order_by(text("objects_counted desc, last_time_updated desc, idle_in_mins asc, cam asc"))
        ResultProxy = conn.execute(query)
        cursor = ResultProxy.fetchall()
        rows = [dict(r) for r in cursor]
        conn.close()
        return rows
    
    def select_all_active_urls(self):
        """
        Query all active (which return some objects) rows in the urls table
        :return:
        """
        conn = self.getConn()
        query = sql.select([self.urls]).where(self.urls.c.objects_counted >= 0).order_by(text("objects_counted desc, last_time_updated desc, idle_in_mins asc, cam asc"))
        ResultProxy = conn.execute(query)
        cursor = ResultProxy.fetchall()
        rows = [dict(r) for r in cursor]
        conn.close()
        return rows
    
    def select_all_active_urls_olderThen_secs(self, secs):
        """
        Query all active (which return some objects) rows in the urls table which are older the in minutes
        :return:
        """
        _time = int(time.time()*1000)
        conn = self.getConn()
        query = sql.select([self.urls]).where(
                                            sql.and_(
                                                self.urls.c.objects_counted >= 0,
                                                self.urls.c.last_time_updated < _time - secs*1000)
                                        ).order_by(text("objects_counted desc, last_time_updated desc, idle_in_mins asc, cam asc"))
        ResultProxy = conn.execute(query)
        cursor = ResultProxy.fetchall()
        rows = [dict(r) for r in cursor]
        conn.close()
        return rows    

    def select_old_urls_which_not_mine_olderThen_secs(self,os, secs):
        """
            Query all urls which older then 1 min and pr not processed by this os
            :return:
        """
        _time = int(time.time()*1000)
        conn = self.getConn()
        query = sql.select([self.urls]).where( sql.and_(
                                                self.urls.c.os != str(os),
                                                self.urls.c.last_time_updated < _time - secs*1000)).order_by(text("objects_counted desc, last_time_updated asc, idle_in_mins asc, cam asc"))
        ResultProxy = conn.execute(query)
        cursor = ResultProxy.fetchall()
        rows = [dict(r) for r in cursor]
        conn.close()
        return rows
    
    def select_old_urls_which_is_mine_olderThen_secs(self,os, secs):
        """
            Query all urls which older then 1 min and pr not processed by this os
            :return:
        """
        _time = int(time.time()*1000)
        conn = self.getConn()
        query = sql.select([self.urls]).where( sql.and_(
                                                self.urls.c.os == str(os),
                                                self.urls.c.last_time_updated < _time - secs*1000)).order_by(text("objects_counted desc, last_time_updated asc, idle_in_mins asc, cam asc"))
        ResultProxy = conn.execute(query)
        cursor = ResultProxy.fetchall()
        rows = [dict(r) for r in cursor]
        conn.close()
        return rows


    def select_urls_which_not_mine(self,os):
        """
            Query all urls which older then 1 min and pr not processed by this os
            :return:
        """
        conn = self.getConn()
        query = sql.select([self.urls]).where( 
                                                self.urls.c.os != str(os)).order_by(text("objects_counted desc, last_time_updated asc, idle_in_mins asc, cam asc"))
        ResultProxy = conn.execute(query)
        cursor = ResultProxy.fetchall()
        rows = [dict(r) for r in cursor]
        conn.close()
        return rows

    def select_nobody_urls(self):
        """
            Query all urls which older then 1 min and pr not processed by this os
            :return:
        """
        conn = self.getConn()
        query = sql.select([self.urls]).where( sql.or_(
                                                self.urls.c.os == '',
                                                self.urls.c.os == None)).order_by(text("objects_counted desc, last_time_updated asc, idle_in_mins asc, cam asc"))
        ResultProxy = conn.execute(query)
        cursor = ResultProxy.fetchall()
        rows = [dict(r) for r in cursor]
        conn.close()
        return rows

    def check_if_cam_in_processing(self, os, id, secs):
        conn = self.getConn()
        _time = int(time.time()*1000)    
        query = sql.select([self.urls]).where( sql.and_(
                                                self.urls.c.os != os,
                                                self.urls.c.id == id,
                                                self.urls.c.last_time_updated > _time - secs*1000 ))
        
        ResultProxy = conn.execute(query)
        cursor = ResultProxy.fetchall()
        
        return len(cursor)


    def select_old_urls(self):
        """
            Query all urls which older then 1 min 
            :return:
        """
        _time = int(time.time()*1000)
        conn = self.getConn()
        query = sql.select([self.urls]).where(
                                                self.urls.c.currentime < _time - 60000).order_by(text("objects_counted desc, last_time_updated asc, idle_in_mins asc, cam asc")) 
        ResultProxy = conn.execute(query)
        cursor = ResultProxy.fetchall()
        rows = [dict(r) for r in cursor]
        conn.close()
        return rows


    
    def insert_urls(self, params):
        conn = self.getConn()
        row = None
        try:
            query = sql.insert(self.urls)
            ResultProxy = conn.execute(query, params)
   
            for result in ResultProxy: row  = result
            logging.debug(" insert_urls was {0} with params: {1}".format(ResultProxy.is_insert ,params))
        except Exception as e:
            logging.debug(" e: {}".format( e))
            raise e
        finally:
            conn.close()            
        return row 

    def update_urls(self, params):
        conn = self.getConn()
        logging.debug(" before update_urls  params: {}".format(params))        
        try:
            if 'id' in params:
                query = sql.update(self.urls).where(self.urls.c.id == params['id']).values(params)
            else:    
                query = sql.update(self.urls).where(self.urls.c.url == params['url']).values(params)
            ResultProxy = conn.execute(query)
            logging.debug(" update_urls was {} with params: {}".format(ResultProxy.is_insert ,params))
        except Exception as e:
            logging.debug(" e: {}".format( e))
            raise e
        finally:
            conn.close() 

    def delete_urls(self, params):
        conn = self.getConn()
        try:
            query = sql.delete(self.urls).where(sql.or_( self.urls.c.id == params['id'] , 
                                                        self.urls.c.id == params['url'] ))
            ResultProxy = conn.execute(query)
            logging.debug(" delete_urls was {}  with params: {}".format(ResultProxy.is_insert ,params))
        except Exception as e:
            logging.debug(" e: {}".format( e))
            raise e
        finally:
            conn.close() 


# ####################  Statistic operations ######################################## #

    def insert_statistic(self, params):
        conn = self.getConn()
        for param in params:
            hashcodes = ''
            hashcodes = str(param['hashcodes'])
        if param['y'] == 0: return # never store dummy noise
        try:
            values = {'type': param['name'],'currentime': param['x'], 'y': param['y'], 'hashcodes': hashcodes, 'cam':param['cam'] }     
            query = sql.insert(self.statistic)
            ResultProxy = conn.execute(query, values)
            logging.debug(" insert_statistic was {0} with params: {1}".format(ResultProxy.is_insert ,params))    
        except Exception as e:
            logging.debug(" e: {}".format( e))
        finally:
            conn.close()     


    def select_statistic_by_time(self, cam, time1, time2, obj):
        """
        Query statistic by time
        :param conn: the Connection object
        :param time1, time2 in second INTEGER
        :return:
        """
        now = time.time()
        time2 = int((now - time2*3600)*1000)
        time1 = int((now - time1*3600)*1000)
        if time2 > time1:  # swap them 
            a=time2
            time2=time1 
            time1=a

        logging.debug(time2,time1, obj)
        tuple_ =  obj.split(',')
        #logging.debug(str)
        #cur.execute("SELECT type, currentime as x0, currentime + 30000 as x, y as y FROM statistic filter type IN" +str+ " AND cam="+self.P+" AND currentime BETWEEN "+self.P+" and "+self.P+" ORDER BY type,currentime ASC", #DeSC
        #    (cam, time2, time1 ))

        query = sql.select([self.statistic]).where(sql.and_(self.statistic.columns.cam == cam, 
                                                              self.statistic.columns.currentime < time1,
                                                              self.statistic.columns.currentime > time2, 
                                                              self.statistic.columns.type.in_(tuple_)
                                                              
                                                             )
                                                    ).order_by(text("currentime asc"))
        conn = self.getConn()                                            
        ResultProxy = conn.execute(query)
        cursor = ResultProxy.fetchall()    
        conn.close()
        # convert row object to the dictionary
        #cursor = cur.fetchall()
        _type = ""
        rows=[]
        for record in cursor:
                type = record[0]
                if(type != _type): 
                    rows.append({'label':record[0],'values': 
                    [ {'x0':v[1], 'x':v[1] + 30000,'y':v[2], 'hashcodes':v[3]} for v in list(filter( lambda x : x[0] == type , cursor))] })
                _type=type
        #logging.debug(rows)
        return rows

# ####################  Objects operations ######################################## #

    def select_all_objects(self, cam):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        conn = self.getConn()
        query = sql.select([self.objects]).where( self.objects.c.cam  == cam                                                          
                                                ).order_by(text("currentime desc")).limit(self.limit).offset(0)
        ResultProxy = conn.execute(query)
        cursor = ResultProxy.fetchall()
        rows = [dict(r) for r in cursor]
        conn.close()
        return rows

    def select_objects(self, cam, hashcodes):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        conn = self.getConn()
        # Remove spaces
        hashcodes = re.sub(r'\s', '', hashcodes)
        # Split by comma and convert to array of integers
        hashcodes_array = list(map(int, hashcodes.split(',')))
        
  
        print("hashcodes: {} ".format(hashcodes))
        query = sql.select([self.objects]).where( self.objects.c.hashcode.in_(hashcodes_array)                                                       
                                                ).order_by(text("currentime desc")).limit(self.limit).offset(0)
        ResultProxy = conn.execute(query)
        cursor = ResultProxy.fetchall()
        rows = [dict(r) for r in cursor]
        conn.close()
        return rows

    def insert_frame(self, hashcode, date, time, type, numpy_array, startX, startY, x_dim, y_dim, cam):
        
        if y_dim <49 or x_dim <49 or x_dim/y_dim > 4.7 or y_dim/x_dim > 4.7: return
        #cur.execute("UPDATE objects SET currentime="+self.P+" WHERE hashcode="+self.P, (time, str(hashcode)))
        #logging.debug("cam= {}, x_dim={}, y_dim={}".format(cam, x_dim, y_dim))
        buffer = cv2.imencode('.jpg', numpy_array)[1]
        jpg_as_base64='data:image/jpeg;base64,'+ base64.b64encode(buffer).decode('utf-8')


        conn = self.getConn()
        try:
            #cur.execute("INSERT INTO objects (hashcode, currentdate, currentime, type, frame, x_dim, y_dim, cam) VALUES ("+self.P+", "+self.P+", "+self.P+", "+self.P+", "+self.P+", "+self.P+", "+self.P+", "+self.P+")", 
            #(str(hashcode), date, time, type, str(jpg_as_base64), int(x_dim), int(y_dim), int(cam)))
            values = {'hashcode': hashcode, 'currentdate': date, 'currentime': time, 'type': type, 'frame':str(jpg_as_base64),
                      'width': int(x_dim),'height': int(y_dim), 'x_dim': int(startX), 'y_dim': int(startY) , 'cam':cam}     
            query = sql.insert(self.objects)
            ResultProxy = conn.execute(query, values)
            #logging.debug(" insert_frame was {0} with params: {1}".format(ResultProxy.is_insert ,values))
        except Exception as e: logging.debug(" e: {}".format( e))
        finally:
            conn.close()


    def select_frame_by_time(self, cam, time1, time2):
        """
        Query frames by time
        :param conn: the Connection object
        :param cam, time1, time2 in epoch seconds
        :return:
        """
        now = time.time()
        time2 = int((now - time2*3600)*1000)
        time1 = int((now - time1*3600)*1000)
        if time2 > time1:  # swap them 
            a=time2
            time2=time1 
            time1=a


        #cur.execute("SELECT cam, hashcode, currentdate, currentime, type, frame FROM objects filter cam="+self.P+" AND currentime BETWEEN "+self.P+" and "+self.P+" ORDER BY currentime DESC", (cam,time1,time2,))
        query = sql.select([self.objects]).where(sql.and_(    self.objects.columns.currentime > time2,                                                       
                                                              self.objects.columns.currentime < time1,                                                              
                                                              self.objects.columns.cam == cam
                                                             )
                                                ).order_by(text("currentime desc")).limit(self.limit).offset(0)
        conn = self.getConn()
        ResultProxy = conn.execute(query)
        cursor = ResultProxy.fetchall()
        rows = [dict(r) for r in cursor]
        conn.close()
        return rows

    def select_last_frames(self, cam, time1, time2, obj,  offset=0):
        """
        Query last n rows of frames b
        :param conn: the Connection object
        :param n_rows number of rows restrict value of request
        :return:
        """
        now = time.time()
        time2 = int((now - time2*3600)*1000)
        time1 = int((now - time1*3600)*1000)
        if time2 > time1:  # swap them 
            a=time2
            time2=time1 
            time1=a
        #str =  "('" + obj.replace(",","','") + "')"    
        logging.debug(time2,time1, obj)
        #tuple_ =  obj.split(',')
        
        #cur.execute("SELECT cam, hashcode, currentdate, currentime, type, frame FROM objects filter cam="+self.P+" AND  type IN " +str+ " AND currentime BETWEEN "+self.P+" and "+self.P+" ORDER BY currentime DESC LIMIT "+self.P+" OFFSET "+self.P+"", 
        #    (cam, time2, time1,n_rows,offset,))
        #fetched_rows = cur.fetchall()
        query = sql.select([self.objects]).where(sql.and_(    self.objects.columns.cam == cam,
                                                              self.objects.columns.currentime > time2,                                                       
                                                              self.objects.columns.currentime < time1                                                             
                                                            # do not use it now due to expansive operation:  self.objects.columns.type.in_(tuple_) 
                                                        )
                                                ).order_by(text("currentime desc")).limit(self.limit).offset(offset)
        conn = self.getConn()                                            
        ResultProxy = conn.execute(query)
        cursor = ResultProxy.fetchall()
        conn.close()
        rows = [dict(r) for r in cursor]
        return rows



    def delete_frames_later_then(self, hours):
        """
        Delete all records from objects table which are later then 'hours' back
        """
        # predicate : '-70 minutes' , '-1 seconds ', '-2 hour'
        #cur.execute("DELETE from objects filter currentime < strftime('"+self.P+"','now'," + predicate+ ")")

        millis_back = int(round(time.time() * 1000)) - hours*60*60*1000
        conn = self.getConn()
        try:
            query = sql.delete(self.objects).where( self.objects.currentime < millis_back )
            ResultProxy = conn.execute(query)
            logging.debug(" delete_frames_later_then:  status: {0}  hoours: {1}".format(ResultProxy.is_insert ,hours))
        except Exception as e: logging.debug(" e: {}".format( e))
        finally:
            conn.close()
    
def main():
    database = "framedata.db"

    # create a database connection
    sql = Sql(database)
    conn = sql.getConn() 
 
if __name__ == '__main__':
    main()
