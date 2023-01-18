import time
import logging
import threading

from project.config import  ProductionConfig as prod
from project.classifier import Detection
from project import db, detectors, comp_node



logging.basicConfig(level=logging.INFO)

DELETE_FILES_LATER = 72 #   ( 3 days in hours)
URL_PINGS_NUMBER = 100 # delete URL after that pings

def start():
    time.sleep(1)
    logging.info("[INFO] loading model...")
    # construct a child process *indepedent* from our main process of
    # execution
    logging.info("[INFO] starting process...")
    # initialize the video stream, allow the cammera sensor to warmup,
    # and initialize the FPS counter
    logging.info("[INFO] starting video stream...")
    initialize_video_streams()
    threading.Timer(1200*24, clean_up_service).start() # in  1 days
    threading.Timer(100, lock_urls_for_os).start()  # start after 100 sec 



# initialize the video stream, allow the cammera sensor to warmup,
# and initialize the FPS counter
def initialize_video_streams(url=None, videos=[]):
    i = 0
    global detectors
    arg = None
    if url is not None:
        arg = url
        i = len(videos)
        logging.info('new url:' + url)
    #  initialise picam or IPCam
    else:
        arg = prod.args.get('video_file' + str(i), None)
    logging.info('Video urls:')
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
                logging.info(arg)
    videos_ = db.select_all_urls()
    """ Update all videos as mine , start greeding algorithm here ..."""
    """ Updation """
    logging.info( "Total number of videos ready for update: {}".format(len(videos_)))
    for video in videos_:
        
        params = { 'id': video['id'], 'url': video['url'], 'cam': video['cam'], 'os': comp_node(), 'currentime':time.time()*1000 }
        try:
            logging.info("trying to update where id:{} with cam:{} ,url:{} , os {}".format(params['id'], params['cam'], params['url'], params['os']))
            logging.debug("detectors: " + str(detectors) ) 
            if params['id'] not in detectors:
                """ Make external call ( to Docker gateway if its present) to delegate this video processing to different node"""
                detection = Detection(prod.CLASSIFIER_SERVER, float(prod.CONFIDENCE), prod.args["model"], params)
                logging.DEBUG("A new detection  process was created." + str(detection))                 
                
                detectors[params['id']] = detection
                db.update_urls(params)
                logging.info("p_classifiers for cam: {} started by {} ".format(params['id'], comp_node() ))
             
            
            #url = 'http://{}:{}{}'.format(IP_ADDRESS,port,deny_service_url)
            #p_deny_service = Process(target=deny_service_call, args = (url,params)) #imagesQueue,detectors,prod,IMAGES_BUFFER))
            #p_deny_service.daemon=False
            #p_deny_service.start()
            i = len(detectors)
            if i == prod.MAXIMUM_VIDEO_STREAMS: break
             
        except Exception as e:
            logging.info("Exception {}".format(e))




"""Delete old images later then DELETE_FILES_LATER milliseconds every 24 hours"""  
def clean_up_service():
  db.delete_frames_later_then(DELETE_FILES_LATER)
  threading.Timer(3600*24, clean_up_service).start() # in  3 days




""" Lock urls record for every 101 seconds """
def lock_urls_for_os():
    os = comp_node()
    global detectors
    videos_ = db.select_old_urls()
    logging.debug( "Total number of ready to re-process: {}".format(len(videos_)))
    num = len(detectors) 
    num_detections = num_rm_detections = 0
    for params in videos_:
        """ grab the the videos which was not processed for last 1 min. and start process it from this node """
        if params['id'] not in detectors:          
            params['os'] = os
            logging.info("p_classifiers for cam: {}  re-started by {} ".format(params['id'], params['os'] ))
            try:
                
                detection = Detection(prod.CLASSIFIER_SERVER, float(prod.CONFIDENCE), prod.args["model"], params)
                
                detectors[params['id']] = detection
                num_detections +=1
                logging.info( "Video  {}  assigned  to the node: {}".format(params['id'], os))
                db.update_urls(params)
                 
                   
                if num == prod.MAXIMUM_VIDEO_STREAMS: break

                
            except Exception as e:
                logging.critical("Exception {}".format(e))
    #if video streams not active remove it
    logging.debug( "Detectors:  {}".format(detectors))
    for cam in detectors:
        logging.debug( "Detection[ {} ]:  {}, errors: {}".format(cam,detectors[cam], detectors[cam].errors))                
        # remove all processes which older then 1 min and not pingable ( more then URL_PINGS_NUMBER pinged )
        if( detectors[cam].errors > URL_PINGS_NUMBER  and  (time.time()*1000 - detectors[cam].createdtime) > 60000 ):
            #db.update_urls(cam) do not delete url only update status how many minutess was not active. (time.time()*1000 - detectors[cam].createdtime)/1000
            logging.info("Url {} has been deleted".format(detection.video_url))
            for process in detectors[cam].processes: 
                process.terminate()
            del detectors[cam]
            num_rm_detections +=1

    logging.debug( "Node: {} Total number: {} of an assigned videos ".format(os, num)) 
    logging.debug( "Node: {} Total number of removed videos: {}".format( os, num_rm_detections))
                         
    threading.Timer(1, lock_urls_for_os).start()                


if __name__ == "__main__":
    start()
