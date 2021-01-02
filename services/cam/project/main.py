from multiprocessing import Process
from multiprocessing import Queue
import os
import threading
import argparse
import time
import logging
import mimetypes
import json
import requests
import urllib.request
import urllib.error
import cv2



from project.config import  ProductionConfig as prod
from project.classifier import Detection
from project import db
import platform 
from project.sleep_decorator import sleep

from flask import Blueprint, Response, request, g,redirect, url_for, send_from_directory
from flask_cors import cross_origin, CORS

logger = logging.getLogger('logger')
logger.setLevel(logging.INFO)
console = logging.StreamHandler()
logger.addHandler(console)
logger.debug('DEBUG mode')

@sleep(1)
def delegate_service(url, params=None):  
    try:
        r = requests.post(url,data=params)
        r.raise_for_status()
    except  requests.exceptions.HTTPError as e:
        """ Servicing this video was not denied other nodes satisfied with grabbing this video """
        imagesQueue[params['id']] = Queue(maxsize=IMAGES_BUFFER + 5)

    except urllib.error.HTTPError as e:
        # Email admin / log
        logger.info('HTTPError: {} for {}'.format(e.code,url))
        # Re-raise the exception for the decorator
        raise urllib.error.HTTPError
    except urllib.error.URLError as e:
        # Email admin / log
        logger.info('URLError: {} for {}'.format(e.code,url))
        # Re-raise the exception for the decorator
        raise urllib.error.URLError
    else:  
        """  Website is up
             Service was denied: stop processes associated with this video then remove video from  Queue dictionary """
        if detectors.get(params['id'], None) is not None: del detectors[params['id']]
        if imagesQueue.get(params['id'], None) is not None:del imagesQueue[params['id']]



def comp_node():
    # if its windows
    if os.name == 'nt':
        return  platform.node()
    else:
        return os.uname()[1]

DELETE_FILES_LATER = 8 #   (8hours)
ENCODING = "utf-8"
IMAGES_BUFFER = 100
#  --------------------  constanst and definitions -------------------------
deny_service_url = '/deny_service'


camleft = []
camright = []
videos = []
IMG_PAGINATOR = 40
SHOW_VIDEO = False
port = prod.PORT
IP_ADDRESS = prod.IP_ADDRESS


class CameraMove:
    def __init__(self, move_left, move_right, timestep=10):
        if move_left == None or move_right == None: return
        self.timestep = timestep
        self.move_left = move_left  # 'http://www.google.com' # move_left
        self.move_right = move_right  # 'http://www.google.com' #move_right
        self.t1 = threading.Timer(timestep, self.cameraLoop)
        self.t1.start()

    def cameraLoop(self):
        logger.debug(self.move_left)
        os.system(self.move_left)  # urlopen(self.move_left)
        time.sleep(5.0)
        os.system(self.move_left)  # urlopen(self.move_left)
        time.sleep(5.0)
        os.system(self.move_left)  # urlopen(self.move_left)
        time.sleep(10.0)
        os.system(self.move_right)  # urlopen(self.move_right)
        time.sleep(5.0)
        os.system(self.move_right)  # urlopen(self.move_right)
        time.sleep(5.0)
        os.system(self.move_right)  # urlopen(self.move_right)
        time.sleep(2.0)
        time.sleep(20.0)
        self.t1 = threading.Timer(self.timestep, self.cameraLoop)

        self.t1.start()


main_blueprint = Blueprint("main", __name__)


def change_res(camera, width, height):
    camera.set(3, width)
    camera.set(4, height)


def get_frame(images_queue):
    while True:
        try:
            images_queue.get()
        except:
            continue
        #if SHOW_VIDEO:
        #    cv2.imshow("Camera" + str(cam), images_queue.get())
        #    key = cv2.waitKey(1) & 0xFF



def fetchImagesFromQueueToVideo(filename, imagesQueue):
    # fourcc = cv2.VideoWriter_fourcc(*'DIVX')  # 'x264' doesn't work
    # fourcc = cv2.VideoWriter_fourcc(*'MPEG')
    # fourcc = 0x00000021
    # logger.debug(fourcc)
    # out = cv2.VideoWriter(filename,fourcc, 29.0, size, False)  # 'False' for 1-ch instead of 3-ch for color
    # logger.debug(out)
    # fgbg= cv2.createBackgroundSubtractorMOG2()
    # logger.debug(fgbd)
    while (imagesQueue.qsize() > 2):
        #    fgmask = imagesQueue.get() #fgbg.apply(imagesQueue.get())
        imagesQueue.get()
        # np.save(filename,imagesQueue.get())
    #    out.write(fgmask)
    # cv2.imshow('img',fgmask)
    # out.release()


def destroy():
    # stop the timer and display FPS information
    fps.stop()
    logger.debug("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
    logger.debug("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    # do a bit of cleanup
    #cv2.destroyAllWindows()
    vs.stop()
    #conn.close()



""" 'Global' variables """

args = {}
imagesQueue = {}
detectors = {}
vs = None

fps = None
p_get_frame = None


def start_one_stream_processes(video):
    if imagesQueue.get(video['id'], None) is not None :
        detectors[video['id']] = Detection(prod.CLASSIFIER_SERVER, float(prod.CONFIDENCE), prod.args["model"],
                imagesQueue[video['id']],video)

        logger.info("p_classifiers for cam:" + video['id'] + " started")

  #  p = Process(target=get_frame, args=(imagesQueue[cam], cam))
  #  p.daemon = True
  #  p.start()




def start():
    logger.info("[INFO] loading model...")
    # construct a child process *indepedent* from our main process of
    # execution
    logger.info("[INFO] starting process...")
    # initialize the video stream, allow the cammera sensor to warmup,
    # and initialize the FPS counter
    logger.info("[INFO] starting video stream...")
    videos =  initialize_video_streams()
    for cam in range(0,len(videos)-1):
        start_one_stream_processes(videos[cam])



# initialize the video stream, allow the cammera sensor to warmup,
# and initialize the FPS counter
def initialize_video_streams(url=None, videos=[]):
    i = 0
    #myVideos = []
    arg = None
    if url is not None:
        arg = url
        i = len(videos)
        logger.info('new url:' + url)
    #  initialise picam or IPCam
    else:
        arg = prod.args.get('video_file' + str(i), None)
    logger.info('Video urls:')
    while arg is not None:
        if not (i, arg) in videos:
            #camright.append(prod.args.get('cam_right' + str(i), None))
            #camleft.append(prod.args.get('cam_left' + str(i), None))
            #CameraMove(camright[i], camleft[i])
            params = { 'cam': i, 'url': arg } #, 'os': comp_node()}

            try:
                videos.append(params)
                db.insert_urls(params)
            except: pass  
            finally:
                arg = prod.args.get('video_file' + str(i), None)
                i += 1 
                logger.info(arg)
    videos_ = db.select_all_urls()
    """ Update all videos as mine , start greeding algorithm here ..."""
    for video in videos_:
        params = { 'id': video['id'], 'url': video['url'], 'cam': video['cam'], 'os': comp_node()}
        try:
            logger.info("trying to update where id:{} with cam:{} ,url:{} , os {}".format(params['id'], params['cam'], params['url'], params['os']))
            db.update_urls(params)
            
        except Exception as e:
            logger.info("Exception {}".format(e))
        else:
            url = 'http://{}:{}{}'.format(IP_ADDRESS,port,deny_service_url)
            params['videos_length'] = len(imagesQueue)
            """ Make external call ( to Docker gateway if its present) to delegate this video processing to different node"""
            delegate_service(url, params=params)
           # p_caller = Process(target=delegate_service, args=(url, params))
           # p_caller.daemon = True
           # p_caller.start()
            
 
            
                 
            
    videos = db.select_all_urls()            
    
    logger.info(videos)
    # Start process
    #time.sleep(1.0)
    return videos

def detect(cam):
    """Video streaming generator function."""
    try:
        # logger.debug('imagesQueue:', imagesQueue.empty())
        while True:
            while (not imagesQueue[cam].empty()):
                frame = imagesQueue[cam].get(block=True)
                iterable = cv2.imencode('.jpg', frame)[1].tobytes()
                yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + iterable + b'\r\n'
    except GeneratorExit:
        pass


###################### Flask API #########################

#main_blueprint.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy   dog'
#main_blueprint.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(main_blueprint, resources={r"/urls": {"origins": 'http://localhost:{}'.format(port)}})



# api = Api(main_blueprint)
# api.decorators=[cors.crossdomain(origin='*')]


@main_blueprint.route('/static/<path:filename>')
@cross_origin(origin='http://localhost:{}'.format(port))
def serve_static(filename):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'static', 'js'), filename)


@main_blueprint.route(deny_service_url, methods=['POST'])
@cross_origin(origin='http://localhost:{}'.format(port))
def deny_service():
    params = request.form.to_dict()
    logger.info(params)
    if params['os'] == comp_node():
        return None, 200
    """ if request come rom different node  """
 
    """ Griddy algorithm started here  if  list of videos too big and my list too small """
    if len(imagesQueue) < int(params['videos_length']):
        """ grab this video """
        try:
            params['os'] =  comp_node()
            logger.info("trying to update where id: {} with  url:{} os: {}".format(params['id'], params['url'], params['os']))
            db.update_urls(params)
                      
        except Exception as e:
            logger.info("Exception {}".format(e))
        else:
            """ Signal to request initiator to remove this video from his list and add to this node list"""
            imagesQueue[params['id']] = Queue(maxsize=IMAGES_BUFFER + 5) 
            return None, 412
    return None, 200      
                
   


@main_blueprint.route('/video_feed', methods=['GET'])
@cross_origin(origin='http://localhost:{}'.format(port))
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    
    cam = request.args.get('cam', default=0, type=str)
    if imagesQueue.get(cam, None) is None:
        redirect(url_for('main.video_feed'))
    else:    
        return Response(detect(cam),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@main_blueprint.route('/moreparams')
@cross_origin(origin='http://localhost:{}'.format(port))
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
    print("cam: {}, hour_back:{}, now_in_seconds:{}".format(cam, hour_back1, hour_back2))

    params = gen_params(cam=cam, time1=hour_back1, time2=hour_back2 ,object_of_interest=object_of_interest)
    return Response(params, mimetype='text/plain')


@main_blueprint.route('/moreimgs')
@cross_origin(origin='http://localhost:{}'.format(port))
def moreimgs():
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
    print("cam: {}, hour_back1:{}, hour_back2:{}, object_of_interest: {}".format(cam, hour_back1, hour_back2, object_of_interest))
    rows = db.select_last_frames(cam=cam, time1=hour_back1, time2=hour_back2, obj=object_of_interest)
    return Response(json.dumps(rows,default=str), mimetype='text/plain')


@main_blueprint.route('/imgs_at_time')
@cross_origin(origin='http://localhost:{}'.format(port))
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
    logger.debug(ret)
    return ret


def ping_video_url(url):
    """ Ping url """
    try:
        vs = cv2.VideoCapture(url)
        flag, frame = vs.read()
        ret = flag
    except:
        ret = False
    return flag

@main_blueprint.route('/urls', methods=['GET', 'POST'])
@cross_origin(origin='http://localhost:{}'.format(port))
def urls():
    """Add/Delete/Update a new video url, list all availabe urls."""
    list_url = request.args.get('list', default=None)
    add_url = request.args.get('add', default=None)
    deleted_id = request.args.get('delete', default=None)
    updated_url = request.args.get('updated', default=None)
    cam_id = request.args.get('id', default=None)

    if add_url is not None:
        logger.info('adding a new video urls ' + add_url)
        if ping_video_url(add_url):
            before = len(videos)
            videos = initialize_video_streams(add_ur,videos)
            after = len(videos)
            if before < after: 
                start_one_stream_processes(videos[after -1 ] )
                return Response('{"message":"URL added successfully"}', mimetype='text/plain')
            else:
                return Response('{"message":"URL already exist it was  added successfully before"}', mimetype='text/plain')  
        else:
            return Response('{"message":"URL has no video"}', mimetype='text/plain')

    elif list_url is not None:
        url_list = db.select_all_urls() 
        return Response(json.dumps(url_list, default=str), mimetype='text/json')
        
    elif deleted_id is not None:
        for video in videos:
            if video["id"] == deleted_id:
                videos.remove(video)
            try:
                db.delete_url_by_id(deleted_id)
                return Response('{"message":"URL deleted successfully"}', mimetype='text/plain')
            except:
                return None, 500
    elif updated_url is not None:
        for video in videos:
            if video["id"] == cam_id:
                video["url"] = updated_url
            try:
                params = {'id': cam_id, 'url': updated_url,  'os': os.uname()[1]}
                db.update_urls(params)
            except:
                return None, 500
        return Response('{"message":"URLs updated successfully"}', mimetype='text/plain')



@main_blueprint.route('/params_feed')
@cross_origin(origin='http://localhost:{}'.format(port))
def params_feed():
    """Parameters streaming route. Put this in the src attribute of an img tag."""
    hours = request.args.get('hour_back1', default=1)
    start_hour = request.args.get('hour_back2', default=0)
    currentime = (time.time() - int(start_hour) * 3600) * 1000
    return Response(gen_params(hours, currentime=currentime),
                    mimetype='text/plain')


