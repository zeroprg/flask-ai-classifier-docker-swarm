import time
import logging
import threading

from project.config import  ProductionConfig as prod
from project.classifier import Detection
from project import db, detectors, comp_node


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

DELETE_FILES_LATER = 3*24*3600000 #   ( 3 days in miliseconds)


def start():
    time.sleep(1)
    logger.info("[INFO] loading model...")
    # construct a child process *indepedent* from our main process of
    # execution
    logger.info("[INFO] starting process...")
    # initialize the video stream, allow the cammera sensor to warmup,
    # and initialize the FPS counter
    logger.info("[INFO] starting video stream...")
    initialize_video_streams()
    threading.Timer(3600*24, clean_up_service).start() # in  3 days
    threading.Timer(100, lock_urls_for_os).start()  # start after 100 sec 



# initialize the video stream, allow the cammera sensor to warmup,
# and initialize the FPS counter
def initialize_video_streams(url=None, videos=[]):
    i = 0
    
    arg = None
    if url is not None:
        arg = url
        i = len(videos)
        logger.info('new url:' + url)
    #  initialise picam or IPCam
    else:
        arg = prod.args.get('video_file' + str(i), None)
    logger.info('Video urls:')
    """ Insertion """
    while arg is not None:
        if not (i, arg) in videos:
            #camright.append(prod.args.get('cam_right' + str(i), None))
            #camleft.append(prod.args.get('cam_left' + str(i), None))
            #CameraMove(camright[i], camleft[i])
            params = { 'cam': i, 'url': arg ,'os': comp_node()}

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
    """ Updation """
    for video in videos_:
        
        params = { 'id': video['id'], 'url': video['url'], 'cam': video['cam'], 'os': comp_node(), 'currentime':time.time()*1000 }
        try:
            logger.debug("trying to update where id:{} with cam:{} ,url:{} , os {}".format(params['id'], params['cam'], params['url'], params['os']))
            if params['id'] not in detectors: #and video['currentime'] > time.time()*1000 - 60000:
                db.update_urls(params)            
        except Exception as e:
            logger.info("Exception {}".format(e))
        else:            
            params['videos_length'] = len(detectors)
            """ Make external call ( to Docker gateway if its present) to delegate this video processing to different node"""
            #deny_service(url, params=params, imagesQueue=imagesQueue, detectors=detectors)
            #imagesQueue[params['id']] = Queue(maxsize=IMAGES_BUFFER + 5)
            
            detection = Detection(prod.CLASSIFIER_SERVER, float(prod.CONFIDENCE), prod.args["model"], params)
            
            #if video stream not active remove it 
            if( detection.errors == 0 ):
                detectors[params['id']] = detection
            else:
                db.delete_urls(params)
                
    
                
                
            logger.info("p_classifiers for cam: {} started by {} ".format(video['id'], comp_node() ))
            
            #url = 'http://{}:{}{}'.format(IP_ADDRESS,port,deny_service_url)
            #p_deny_service = Process(target=deny_service_call, args = (url,params)) #imagesQueue,detectors,prod,IMAGES_BUFFER))
            #p_deny_service.daemon=False
            #p_deny_service.start()
            i = len(detectors)
            if i == prod.MAXIMUM_VIDEO_STREAMS: break
                
            
    videos = db.select_all_urls()            

    logger.info(videos)
    # Start process
    #time.sleep(1.0)
    return videos



"""Delete old images later then DELETE_FILES_LATER milliseconds every 24 hours"""  
def clean_up_service():
  db.delete_frames_later_then(DELETE_FILES_LATER)
  threading.Timer(3600*24, clean_up_service).start() # in  3 days




""" Lock urls record for every 101 seconds """
def lock_urls_for_os():
  
  #db.update_url_by_os(comp_node())
  videos_ = db.select_all_urls()

  for params in videos_:
        """ grab the the videos which was not processed for last 10 min. and start process it from this node """
        if params['id'] not in detectors:
           
            params['os'] = comp_node()
            logger.info("p_classifiers for cam: {}  re-started by {} ".format(params['id'], params['os'] ))
            try:
                db.update_urls(params)
            except Exception as e:
                logger.critical("Exception {}".format(e))
            else:
                 
                detection = Detection(prod.CLASSIFIER_SERVER, float(prod.CONFIDENCE), prod.args["model"], params)
                
                #if video stream not active remove it 
                if( detection.errors == 0 ):
                    detectors[params['id']] = detection
                else:
                    db.delete_urls(params)
                    logger.info("Url {} has been deleted".format(params['url']))
                    
                i = len(detectors)    
                if i == prod.MAXIMUM_VIDEO_STREAMS: break
  threading.Timer(100, lock_urls_for_os).start()                


if __name__ == "__main__":
    start()
