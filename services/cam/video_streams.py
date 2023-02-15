import time
import logging
import threading


from project.config import  ProductionConfig as prod
from project.classifier import Detection
from project import db, populate_lat_long, detectors, comp_node, DELETE_FILES_LATER, clean_up_service_interval, update_urls_from_stream_interval, delete_expired_streams_interval



logging.basicConfig(level=logging.INFO)


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
    
    threading.Timer(clean_up_service_interval, clean_up_service).start() # in  3 days 
    threading.Timer(delete_expired_streams_interval, delete_expired_streams).start()
    threading.Timer(update_urls_from_stream_interval, update_urls_from_stream).start()

# initialize the video stream, allow the cammera sensor to warmup,
# and initialize the FPS counter
def initialize_video_streams(url=None, videos=[]):
    i = 0
    #global detectors
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
    videos_ = db.select_all_active_urls_olderThen_secs(5)
    """ Update all videos as mine , start greeding algorithm here ..."""
    """ Updation """
    logging.info( "Total number of videos ready for update: {}".format(len(videos_)))
    for video in videos_:
        
        params = { 'id': video['id'], 'url': video['url'], 'cam': video['cam'], 'os': comp_node(), 'currentime':time.time()*1000 }
        populate_lat_long(params)
        try:
            logging.info("trying to update where id:{} with cam:{} ,url:{} , os {}".format(params['id'], params['cam'], params['url'], params['os']))
            logging.debug("detectors: " + str(detectors) ) 
            if params['id'] not in detectors:
                """ Make external call ( to Docker gateway if its present) to delegate this video processing to different node"""
                db.update_urls(params)
                detection = Detection(prod.CLASSIFIER_SERVER, float(prod.CONFIDENCE), prod.args["model"], params)             
                
                detectors[params['id']] = detection
                logging.info("A new detection  process was created." + str(detection))                 
                logging.info("p_classifiers for cam: {} started by {} ".format(params['id'], comp_node() ))
             
            
            #url = 'http://{}:{}{}'.format(IP_ADDRESS,port,deny_service_url)
            #p_deny_service = Process(target=deny_service_call, args = (url,params)) #imagesQueue,detectors,prod,IMAGES_BUFFER))
            #p_deny_service.daemon=False
            #p_deny_service.start()
            
            if len(detectors) >= prod.MAXIMUM_VIDEO_STREAMS: break
             
        except Exception as e:
            logging.critical("Exception {}".format(e))



"""Delete old images later then DELETE_FILES_LATER milliseconds every 24 hours"""  
def clean_up_service():
  db.delete_frames_later_then(DELETE_FILES_LATER)
  threading.Timer( clean_up_service , clean_up_service).start() # in  3 days


def delete_expired_streams():
    os = comp_node()
    del_cam = []
    # Create a copy of the detectors dictionary to avoid modifying the original
    # during iteration
    detectors_copy = detectors.copy()
    # Delete terminated process
    for cam in detectors_copy:
        for process in detectors_copy[cam].processes:
            if not process.is_alive(): # at least one is dead kill all
                logging.info( "Detection process {} assigned  to the node: {} was deleted".format(detectors_copy[cam], os))
                del_cam.append(cam)
        # delete detector as soon someone else process it        
        if db.check_if_cam_in_processing(os, cam, update_urls_from_stream_interval) > 0:
            del_cam.append(cam)       
        # update existed processes into db
        #params = { 'id': cam, 'os': comp_node(), 'last_time_updated':time.time()*1000 }
        #db.update_urls(params)
    for cam in del_cam:
        del detectors[cam]          
    threading.Timer(delete_expired_streams_interval, delete_expired_streams).start()


"""Create a new Detections (Process) and update a expired videos with latest update time """
def update_urls_from_stream():
   # global detectors
    # update last_time_updated and object_counted from the time when the process was started
    params = {}
    currenttime=time.time()*1000
    os = comp_node()
    params['idle_in_mins'] = 0 
    params['os'] = os

    
    for cam in detectors:
        detection = detectors[cam]
        params['last_time_updated'] = currenttime        
        params['id'] = cam
        db.update_urls(params)
        logging.debug("url update with params: {}".format(params))
    # consider if URL was not updated buy Detection process more then 3 intervals of processing time
    videos_ = db.select_old_urls_which_not_mine_olderThen_secs(os,update_urls_from_stream_interval)
    for params in videos_:
        if len(detectors)  >= prod.MAXIMUM_VIDEO_STREAMS: break
        cam = params['id']
        params['os'] = os
        params['idle_in_mins'] = 0
        populate_lat_long(params)
        try:
            if cam not in detectors:          
                logging.info("p_classifiers for cam: {}  re-started by {} ".format(params['id'], os ))
                detection = Detection(prod.CLASSIFIER_SERVER, float(prod.CONFIDENCE), prod.args["model"], params)
                detectors[cam] = detection
                params['last_time_updated'] = currenttime
                params['objects_counted'] = 0
                db.update_urls(params)              
                logging.info( "Video  {}  assigned  to the node: {}".format(params['id'],  params['os']))
        except Exception as e:
            logging.critical("Exception in Detection creation with url{} , e: {}".format(params['url'], e))
    threading.Timer(update_urls_from_stream_interval, update_urls_from_stream).start()            


if __name__ == "__main__":
    start()
