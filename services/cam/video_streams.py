import time
import logging
import threading
import requests
import socket
from urllib.parse import urlsplit

from project.config import  ProductionConfig as prod
from project.classifier import Detection
from project import db, detectors, comp_node, DELETE_FILES_LATER, clean_up_service_interval, update_urls_from_stream_interval, delete_expired_streams_interval



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
    videos_ = db.select_all_active_urls()
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
            if i >= prod.MAXIMUM_VIDEO_STREAMS: break
             
        except Exception as e:
            logging.info("Exception {}".format(e))




"""Delete old images later then DELETE_FILES_LATER milliseconds every 24 hours"""  
def clean_up_service():
  db.delete_frames_later_then(DELETE_FILES_LATER)
  threading.Timer( clean_up_service , clean_up_service).start() # in  3 days


"""  Delete terminated processes and processes with not active urls """
def delete_expired_streams():
    params = {'os': comp_node()}
    del_cam = None
    # Delete terminated process
    for cam in detectors:
        for process in detectors[cam].processes:
            if( process.is_alive() == False): # at least one is dead kill all
                logging.debug( "Detection process {} assigned  to the node: {} was deleted".format(detectors[cam], params['os']))
                del_cam = cam
                break
    if( del_cam is not None): del detectors[del_cam]              
    threading.Timer(delete_expired_streams_interval, delete_expired_streams).start()

"""Create a new Detections (Process) and update a expired videos with latest update time """
def update_urls_from_stream():
   # global detectors
    # update last_time_updated and object_counted from the time when the process was started
    params = {}
    currenttime=time.time()*1000
    params['os'] = comp_node()
    params['idle_in_mins'] = 0 

    
    for cam in detectors:
        detection = detectors[cam]
        params['last_time_updated'] = currenttime        
        params['id'] = cam
        db.update_urls(params)
        logging.debug("url update with params: {}".format(params))
    # consider if URL was not updated buy Detection process more then 3 intervals of processing time
    videos_ = db.select_all_active_urls_olderThen_secs(3*update_urls_from_stream_interval)
    for params in videos_:
        if len(detectors)  >= prod.MAXIMUM_VIDEO_STREAMS: break
        cam = params['id']
        params['os'] = comp_node()
        params['idle_in_mins'] = 0
        populate_lat_long(params)
        try:
            if cam not in detectors:          
                logging.info("p_classifiers for cam: {}  re-started by {} ".format(params['id'], params['os'] ))
                detection = Detection(prod.CLASSIFIER_SERVER, float(prod.CONFIDENCE), prod.args["model"], params)
                detectors[cam] = detection
                params['last_time_updated'] = currenttime
                params['objects_counted'] = 0
                db.update_urls(params)              
                logging.debug( "Video  {}  assigned  to the node: {}".format(params['id'],  params['os']))
        except Exception as e:
            logging.critical("Exception in Detection creation with url{} , e: {}".format(params['url'], e))
    threading.Timer(update_urls_from_stream_interval, update_urls_from_stream).start()            

def populate_lat_long(params):
    data = get_geolocation_by_ip(convert_url_to_ip(params['url']))

    params['lat'] = data['location']['lat']
    params['lng'] = data['location']['lng']
    params['city'] =  data['location']['city']
    params['postalcode'] =  data['location']['postalCode']
    params['country'] =  data['location']['country']
    

ip_geolocation_key = None
def get_geolocation_by_ip(ip): 
    global ip_geolocation_key
    if( ip_geolocation_key is None):
        with open('api_key.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                if 'ip_geolocation' in line.lower():
                    ip_geolocation_key = line.strip().split('=')[1]
                    break
    print(f"IP address: {ip}")
    headers = {
        "X-RapidAPI-Key": ip_geolocation_key,
        "X-RapidAPI-Host": "whoisapi-ip-geolocation-v1.p.rapidapi.com"
    }
    json_response = None
    url = "https://whoisapi-ip-geolocation-v1.p.rapidapi.com/api/v1?ipAddress={}".format(ip)
    try:
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()
        json_response = response.json()
        logging.debug("Entire JSON response: %s", json_response)
    except requests.exceptions.HTTPError as http_err:
        print("HTTP error occurred: %s", http_err)
    except Exception as err:
        print("Failed to get geolocation by IP: %s", err)
    return json_response

def get_hostname(url):
    result = urlsplit(url)
    return result.hostname

def convert_url_to_ip(url):
    try:        
        hostname = get_hostname(url)
        logging.debug("convert_url_to_ip: {}".format(hostname))
        if(hostname is None): return None
        return socket.gethostbyname(hostname)
    except socket.gaierror as e:
        logging.critical(f"Error resolving hostname: {e}")
        return None
    
google_api_key = None
def search_with_google(query):
    global google_api_key
    if( google_api_key is None):
        with open('api_key.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                if 'google_search' in line.lower():
                    google_api_key = line.strip().split('=')[1]
                    break

    url = "https://www.googleapis.com/customsearch/v1?q={}&key={}".format(query, google_api_key)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        items = data.get("items", [])
        urls = [item.get("link", "") for item in items]
        return urls
    else:
        return []
  

if __name__ == "__main__":
    start()
