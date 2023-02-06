import time
import os
import cv2
import json
import logging

from project.config import  ProductionConfig as prod
from project import db, comp_node, videos


from flask import Blueprint, Response, request, send_from_directory
from flask_cors import cross_origin, CORS

logging.basicConfig(level=logging.INFO)


ENCODING = "utf-8"

#  --------------------  constanst and definitions -------------------------
IMG_PAGINATOR = 40

port =  prod.PORT
IP_ADDRESS = prod.DB_IP_ADDRESS


main_blueprint = Blueprint("main", __name__)


def change_res(camera, width, height):
    camera.set(3, width)
    camera.set(4, height)



###################### Flask API #########################

#main_blueprint.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy   dog'
#main_blueprint.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(main_blueprint)



# api = Api(main_blueprint)
# api.decorators=[cors.crossdomain(origin='*')]

@main_blueprint.route("/ping", methods=["GET"])
def ping_pong():    
    logging.info('Hitting the "/ping" route')
    node = os.uname()[1]
    if os.name == 'nt':
        node = 'Windows'
    return Response(json.dumps({"status": "success", "message": "ping-pong!", "container_id": node},
                               default=str, indent = 4), mimetype='text/plain', status=200)

@main_blueprint.route('/static/<path:filename>')
@cross_origin(origin='*')
def serve_static(filename):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'static', 'js'), filename)

@main_blueprint.route('/health')
def health():
    
    with db.engine.connect() as conn:
        objects_rows = conn.execute("SELECT count(*) FROM OBJECTS" ).fetchall()
        print("Total objects : {}".format(objects_rows[0][0]))
        statistic_rows = conn.execute("SELECT count(*) FROM STATISTIC" ).fetchall()
        print("Total statistic : {}".format(statistic_rows[0][0]))
        print("Database connection health was fine !!!")  


    ret = {'os': comp_node(), "Total objects": objects_rows[0][0],  "statistic table rows": statistic_rows[0][0]}
    logging.info(ret)
    return Response(json.dumps(ret,default=str, indent = 4), mimetype='text/plain', status=200)



@main_blueprint.route('/moreparams')
def moreparams():
    """ Read list of json files or return one specific  for specific time """
    hour_back1 = request.args.get('hour_back1', default=1, type=int)
    hour_back2 = request.args.get('hour_back2', default=0, type=int)
    object_of_interest = request.args.get('object_of_interest', type=None)
    #print("object_of_interest: " + str(object_of_interest)[1:-1])

    cam = request.args.get('cam', default=0, type=str)
    if hour_back1 != '':
        hour_back1 = int(hour_back1)
    else:
        hour_back1 = 0  # default value: 60 min back

    if hour_back2 != '':
        hour_back2 = int(hour_back2)
    else:
        hour_back2 = 1  # default value: 60 min back
    logging.debug("cam: {}, hour_back:{}, now_in_seconds:{}".format(cam, hour_back1, hour_back2))

    params = gen_params(cam=cam, time1=hour_back1, time2=hour_back2 ,object_of_interest=object_of_interest)
    return Response(params, mimetype='text/plain')


@main_blueprint.route('/moreimgs')
def moreimgs():
    """ Read list of json files or return one specific  for specific time """
    hour_back1 = request.args.get('hour_back1', default=0, type=int)
    hour_back2 = request.args.get('hour_back2', default=1, type=int)
    object_of_interest = request.args.get('object_of_interest', type=None)
    #print("object_of_interest: " + str(object_of_interest)[1:-1])

    cam = request.args.get('cam', default=0, type=str)
    if hour_back1 != '':
        hour_back1 = int(hour_back1)
    else:
        hour_back1 = 0  # default value: 60 min back

    if hour_back2 != '':
        hour_back2 = int(hour_back2)
    else:
        hour_back2 = 1  # default value: 60 min back
    print("cam: {}, hour_back1:{}, hour_back2:{}, object_of_interest: {}".format(cam, hour_back1, hour_back2, object_of_interest))
    rows = db.select_last_frames(cam=cam, time1=hour_back1, time2=hour_back2, obj=object_of_interest)
    return Response(json.dumps(rows,default=str), mimetype='text/plain')


@main_blueprint.route('/imgs_at_time')
def imgs_at_time():
    """ Read list of json files or return one specific  for specific time """
    seconds = request.args.get('time', default=int(time.time()*1000), type=int)
    delta = request.args.get('delta', default=10000, type=int)
    cam = request.args.get('cam', default=0, type=str)
    return Response(gen_array_of_imgs(cam, delta=delta, currentime=seconds), mimetype='text/plain')


def gen_array_of_imgs(cam, delta=10000, currentime=int(time.time()*1000)):
    time1 = currentime - delta
    time2 = currentime + delta
    rows = db.select_frame_by_time(cam, time1, time2)
    x = json.dumps(rows, default=str)
    return x



def gen_params(cam='', time1=0, time2=5*60*60*1000, object_of_interest=[]):
    """Parameters streaming generatorcd .. function."""
 
    print("time1: {} time2: {}".format(time1, time2))
    ls = db.select_statistic_by_time(cam, time1, time2, object_of_interest)
    ret = json.dumps(ls, default=str)  # , indent = 4)
    logging.debug(ret)
    return ret


def ping_video_url(url):
    """ Ping url """
    try:
        vs = cv2.VideoCapture(url)
        flag, _ = vs.read()
    except Exception as e:        
        logging.critical("Exception in ping url: {}".format(e))   
        
    return flag


@main_blueprint.route('/urls', methods=['POST'])
def add_urls():
    payload = request.get_json()    
    logging.debug("request payload: {} ".format(payload))
    add_url = payload['add']
    logging.debug("add_url: {} ".format(add_url))
    if add_url is not None:
            logging.info('adding a new video urls ' + add_url)
            if ping_video_url(add_url):
                try:
                    params = { 'url': add_url }
                    db.insert_urls(params)
                except Exception as e:
                    logging.critical("Exception during saving url:{} : {}".format(add_url,e))
                    msg = "URL already exist it was already  added successfully"
                    return Response({"message":msg}, mimetype='text/plain', status=500)           
                else:     
                    logging.info("URL {} added successfully".format(add_url))           
                    return Response('{"message":"URL added successfully"}', mimetype='text/plain',status=200)
            else:
                logging.info("URL {} has no video".format(add_url))
                return Response('{"message":"URL has no video"}', mimetype='text/plain',status=400)

@main_blueprint.route('/urls', methods=['PUT'])
def update_urls():
    payload = request.get_json()    
    logging.debug("request payload: {} ".format(payload))

    if update_url is not None:
        try:   
            db.update_urls(payload)
        except Exception as e:
            logging.critical("Exception during saving payload: {} : {}".format(payload,e))
            msg = "URL {} with id {} can't be updated successfully".format(payload['url'],payload['id'])
            return Response({"message":msg}, mimetype='text/plain', status=500)           
        else:     
            logging.info("URL {} added successfully".format(payload['url']))           
            return Response('{"message":"URL updated successfully"}', mimetype='text/plain',status=200)
 

@main_blueprint.route('/urls', methods=['GET'])
def urls():
    """Add/Delete/Update a new video url, list all availabe urls."""
    list_url = request.args.get('list', default=None)
    delete_url = request.args.get('delete', default=None)
    updated_url = request.args.get('updated', default=None)
    cam_id = request.args.get('id', default=None)
    logging.debug("list_url:{} delete_url: {} updated_url: {} cam_id:{} ".format(list_url, delete_url, updated_url, cam_id))

   
    if list_url is not None:
        url_list = db.select_all_urls() 
        return Response(json.dumps(url_list, default=str), mimetype='text/json')
        
    elif delete_url is not None:
        for video in videos:
            if video["url"] == delete_url:
                videos.remove(video)
                params = {'url': delete_url}    
                try:
                    db.delete_urls(params)
                    return Response('{"message":"URL deleted successfully"}', mimetype='text/plain')
                except:
                    return None, 500




@main_blueprint.route('/params_feed')
def params_feed():
    """Parameters streaming route. Put this in the src attribute of an img tag."""
    hours = request.args.get('hour_back1', default=1)
    start_hour = request.args.get('hour_back2', default=0)
    currentime = (time.time() - int(start_hour) * 3600) * 1000
    return Response(gen_params(hours, currentime=currentime),
                    mimetype='text/plain')


