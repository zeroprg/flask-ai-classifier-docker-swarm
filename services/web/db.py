#import sqlite3
import cv2
import base64
import time
import sqlite3

#P ="%s" 
P ='?' 
def create_connection(db_file, ipaddress=None, database="postgress", user="postgress", password="123456"):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        if(  ipaddress is None or ipaddress == ''):
            conn = sqlite3.connect(db_file)
            conn.execute("PRAGMA journal_mode=WAL")
            
        else:
            import psycopg2
            conn = psycopg2.connect(host=ipaddress,database=database,user=user,password=password)  
            P='%s'

    except Exception as e:
        print(e)
    return conn
 
 
def select_all_objects(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT hashcode, currentdate, currentime, type, x_dim, y_dim FROM objects  ORDER BY currentime DESC ")
 
    rows = cur.fetchall()
 
    #for row in rows:
    #    print(row)
    return rows

def insert_statistic(conn, params):
    cur = conn.cursor()
    for param in params:
        hashcodes = ''
        length = len(param['hashcodes'])
       # for i in range(length): hashcodes += str(param['hashcodes'][i]) + ',' if i < length - 1 else str(param['hashcodes'][i])
        hashcodes = str(param['hashcodes'])
    if param['y'] == 0: return # never store dummy noise
    try:
        cur.execute("INSERT INTO statistic(type,currentime,y,text,hashcodes,cam) VALUES ("+P+", "+P+", "+P+", "+P+", "+P+", "+P+")",
         (param['name'], param['x'], param['y'], param['text'], hashcodes, param['cam']))
    except Exception as e:
         print(" e: {}".format( e))
    print(" insert_statistic:  {}".format(params))

def select_statistic_by_time(conn, cam, time1, time2, obj):
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
    cur = conn.cursor()
    # cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    str =  "('" + obj.replace(",","','") + "')"
    #print(str)
    cur.execute("SELECT type, currentime as x0, currentime + 30000 as x, y as y FROM statistic WHERE type IN" +str+ " AND cam="+P+" AND currentime BETWEEN "+P+" and "+P+" ORDER BY type,currentime ASC", #DeSC
        (cam, time2, time1 ))
    # convert row object to the dictionary
    cursor = cur.fetchall()
    _type = ""
    rows=[]
    for record in cursor:
            type = record[0]
            if(type != _type): 
                rows.append({'label':record[0],'values': 
                [ {'x0':v[1], 'x':v[2],'y':v[3]} for v in list(filter( lambda x : x[0] == type , cursor))] })
            _type=type
    #print(rows)
    return rows


def insert_frame(conn, hashcode, date, time, type, numpy_array, x_dim, y_dim, cam):
    cur = conn.cursor()
    if y_dim == 0 or x_dim == 0 or  x_dim/y_dim > 5 or y_dim/x_dim > 5: return
    
    cur.execute("UPDATE objects SET currentime="+P+" WHERE hashcode="+P, (time, str(hashcode)))
    print("cam= {}, x_dim={}, y_dim={}".format(cam, x_dim, y_dim))
    if cur.rowcount == 0:
        buffer = cv2.imencode('.jpg', numpy_array)[1]
        jpg_as_base64='data:image/jpeg;base64,'+ base64.b64encode(buffer).decode('utf-8')
        try:
            cur.execute("INSERT INTO objects (hashcode, currentdate, currentime, type, frame, x_dim, y_dim, cam) VALUES ("+P+", "+P+", "+P+", "+P+", "+P+", "+P+", "+P+", "+P+")", 
            (str(hashcode), date, time, type, str(jpg_as_base64), int(x_dim), int(y_dim), int(cam)))
        except Exception as e: print(" e: {}".format( e))


def select_frame_by_time(conn, cam, time1, time2):
    """
    Query frames by time
    :param conn: the Connection object
    :param cam, time1, time2 in epoch seconds
    :return:
    """
   # conn.row_factory= sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT cam, hashcode, currentdate, currentime, type, frame FROM objects WHERE cam="+P+" AND currentime BETWEEN "+P+" and "+P+" ORDER BY currentime DESC", (cam,time1,time2,))
    rows = [dict(r) for r in cur.fetchall()] 
    return rows

def select_last_frames(conn, cam, time1, time2, obj, n_rows=50, offset=0):
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
    str =  "('" + obj.replace(",","','") + "')"    
    print(time2,time1, obj)
    cur = conn.cursor()
    cur.execute("SELECT cam, hashcode, currentdate, currentime, type, frame FROM objects where cam="+P+" AND  type IN " +str+ " AND currentime BETWEEN "+P+" and "+P+" ORDER BY currentime DESC LIMIT "+P+" OFFSET "+P+"", 
        (cam, time2, time1,n_rows,offset,))
    fetched_rows = cur.fetchall()
    rows = [ {'cam':v[0] , 'hashcode':v[1],  'currentdate':v[2], 'currentime':v[3], 'type': v[4], 'frame': v[5]} for v in fetched_rows ]
    #print(rows[0])
    return rows



def delete_frames_later_then(conn, predicate):
    """
    Delete all records from objects table which are later then 'predicate'
    predicate : '-70 minutes' , '-1 seconds ', '-2 hour'
    """
    cur = conn.cursor()
    cur.execute("DELETE from objects WHERE currentime < strftime('"+P+"','now'," + predicate+ ")")
 
def main():
    database = "framedata.db"
 
    # create a database connection
    conn = create_connection(database)
    with conn:
        print("1. Query objects by time:")
        select_frame_by_time(conn, "2019-01-01 00:00:00.00.000", "2019-12-31 00:00:00.00.000")
 
        print("2. Query all objects")
        select_all_stats(conn)
 
 
if __name__ == '__main__':
    main()
