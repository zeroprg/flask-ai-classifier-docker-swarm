from multiprocessing import Process
from multiprocessing import Queue
import os
import threading
import argparse
import time
import logging
import mimetypes
import json
import cv2

#from db.api import Sql
from project.config import  ProductionConfig as prod
from project.classifier import Detection
from project import db

from flask import Blueprint, Response, request, g, send_from_directory
from flask_cors import cross_origin, CORS

logger = logging.getLogger('logger')
logger.setLevel(logging.INFO)
console = logging.StreamHandler()
logger.addHandler(console)
logger.debug('DEBUG mode')


DELETE_FILES_LATER = 8 #   (8hours)
ENCODING = "utf-8"
IMAGES_BUFFER = 100


videos = []
camleft = []
camright = []
IMG_PAGINATOR = 40

SHOW_VIDEO = False

port = '3020' #prod.PORT

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


def get_frame(images_queue, cam):
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


separator = "="
args = {}
imagesQueue = []
detections = None
vs = None

fps = None
p_get_frame = None



def start_one_stream_processes(cam):
    Detection(prod.CLASSIFIER_SERVER, float(prod.args["confidence"]), prod.args["prototxt"], prod.args["model"], videos[cam][1],
              imagesQueue[cam], cam)

    logger.info("p_classifiers for cam:" + str(cam) + " started")

    p = Process(target=get_frame, args=(imagesQueue[cam], cam))
    p.daemon = True
    p.start()


def start():
    logger.info("[INFO] loading model...")
    # construct a child process *indepedent* from our main process of
    # execution
    logger.info("[INFO] starting process...")
    # initialize the video stream, allow the cammera sensor to warmup,
    # and initialize the FPS counter
    logger.info("[INFO] starting video stream...")
    initialize_video_streams()
    for cam in range(len(videos)):
        start_one_stream_processes(cam)

# initialize the video stream, allow the cammera sensor to warmup,
# and initialize the FPS counter
def initialize_video_streams(url=None):
    i = 0
    arg = None
    right = None
    left = None
    if url is not None:
        arg = url
        i = len(videos)
    #  initialise picam or IPCam
    else:
        arg = prod.args.get('video_file' + str(i), None)
    while arg is not None:
        if not (i, arg) in videos:
            camright.append(args.get('cam_right' + str(i), None))
            camleft.append(args.get('cam_left' + str(i), None))
            CameraMove(camright[i], camleft[i])
            videos.append((str(i), arg))
            imagesQueue.append(Queue(maxsize=IMAGES_BUFFER + 5))
            i += 1
            arg = args.get('video_file' + str(i), None)

    # Start process
    time.sleep(1.0)
   # fps = FPS().start()



def detect(cam):
    """Video streaming generator function."""
    label = ''
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



@main_blueprint.route('/video_feed', methods=['GET'])
@cross_origin(origin='http://localhost:{}'.format(port))
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    # gen(Camera()),
    cam = request.args.get('cam', default=0, type=int)
    return Response(detect(int(cam)),  # mimetype='text/event-stream')
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@main_blueprint.route('/moreparams')
@cross_origin(origin='http://localhost:{}'.format(port))
def moreparams():
    """ Read list of json files or return one specific  for specific time """
    hour_back1 = request.args.get('hour_back1', default=1, type=int)
    hour_back2 = request.args.get('hour_back2', default=0, type=int)
    object_of_interest = request.args.get('object_of_interest', type=None)
    #print("object_of_interest: " + str(object_of_interest)[1:-1])

    cam = request.args.get('cam', default=0, type=int)
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

    cam = request.args.get('cam', default=0, type=int)
    if hour_back1 != '':
        hour_back1 = int(hour_back1)
    else:
        hour_back1 = 0  # default value: 60 min back

    if hour_back2 != '':
        hour_back2 = int(hour_back2)
    else:
        hour_back2 = 1  # default value: 60 min back
    print("cam: {}, hour_back1:{}, hour_back2:{}, object_of_interest: {}".format(cam, hour_back1, hour_back2, object_of_interest))
    #db = Sql(DB_IP_ADDRESS)
    rows = db.select_last_frames(cam=cam, time1=hour_back1, time2=hour_back2, obj=object_of_interest)
    return Response(json.dumps(rows,default=str), mimetype='text/plain')


@main_blueprint.route('/imgs_at_time')
@cross_origin(origin='http://localhost:{}'.format(port))
def imgs_at_time():
    """ Read list of json files or return one specific  for specific time """
    seconds = request.args.get('time', default=int(time.time()*1000), type=int)
    delta = request.args.get('delta', default=10000, type=int)
    cam = request.args.get('cam', default=0, type=int)
    return Response(gen_array_of_imgs(cam, delta=delta, currentime=seconds), mimetype='text/plain')


def gen_array_of_imgs(cam, delta=10000, currentime=int(time.time()*1000)):
    time1 = currentime - delta
    time2 = currentime + delta
    #db = Sql(DB_IP_ADDRESS)
    rows = db.select_frame_by_time(cam, time1, time2)
    x = json.dumps(rows, default=str)
    return x


def gen(camera):
    """Video streaming generator function."""
    try:
        while True:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except GeneratorExit:
        pass



def gen_params(cam=0, time1=0, time2=5*60*60*1000, object_of_interest=[]):
    """Parameters streaming generator function."""
 
    print("time1: {} time2: {}".format(time1, time2))
    #db = Sql(DB_IP_ADDRESS)
    ls = db.select_statistic_by_time(cam, time1, time2, object_of_interest)
    ret = json.dumps(ls, default=str)  # , indent = 4)
    logger.debug(ret)
    return ret
def ping_video_url(url):
    video = mimetypes.MimeTypes().guess_type(url)[0]
    if( video =='video/mp4'): return True
    return False

@main_blueprint.route('/urls', methods=['GET', 'POST'])
@cross_origin(origin='http://localhost:{}'.format(port))
def urls():
    print('Hey Im here' )
    """Add/Delete/Update a new video url, list all availabe urls."""
    list_url = request.args.get('list', default=None)
    add_url = request.args.get('add', default=None)
    delete_url = request.args.get('delete', default=None)
    update_url = request.args.get('update', default=None)
    if add_url is not None:
        if ping_video_url(add_url):
            initialize_video_streams(add_url)
            start_one_stream_processes(cam=len(videos) - 1)
            # return index() #redirect("/")
            return Response('{"message":"URL added  successfully , video start processing"}', mimetype='text/plain')            
    print(json.dumps(videos))            
    if list_url is not None:
        #data = {url:videos, objectOfInterests: subject_of_interes}
        #for video in videos:
        return Response(json.dumps(videos), mimetype='text/plain')
        
    if delete_url is not None:
        for video in videos:
            if video[0] == delete_url:
                videos.remove(video)
                return Response('{"message":"URL deleted successfully"}', mimetype='text/plain')
    if update_url is not None:
        index = request.args.get('index', default=None)
        if index is not None:
            videos[index][1] == update_url
            return Response('{"message":"URL updated successfully"}', mimetype='text/plain')


@main_blueprint.route('/params_feed')
@cross_origin(origin='http://localhost:{}'.format(port))
def params_feed():
    """Parameters streaming route. Put this in the src attribute of an img tag."""
    hours = request.args.get('hour_back1', default=1)
    start_hour = request.args.get('hour_back2', default=0)
    currentime = (time.time() - int(start_hour) * 3600) * 1000
    return Response(gen_params(hours, currentime=currentime),
                    mimetype='text/plain')


