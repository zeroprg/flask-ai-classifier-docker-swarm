
import cv2
import imutils
from imutils.video import VideoStream
import requests
from requests.exceptions import HTTPError
import re
import logging
import base64
import time
import json
import numpy as np
import time
import datetime

from multiprocessing import Value
from concurrent.futures import ThreadPoolExecutor


from project import db
from project.caffe_classifier import classify_frame, classify_init
from project import URL_PINGS_NUMBER, update_urls_from_stream_interval, ping_video_url, image_check, simple_decode,topic_rules
from project.statistic import do_statistic


subject_of_interest = ["person", "car"]
DNN_TARGET_MYRIAD = False
executor = ThreadPoolExecutor()
DIMENSION_X = 300
DIMENSION_Y = 300
piCameraResolution = (640, 480)  # (1024,768) #(640,480)  #(1920,1080) #(1080,720) # (1296,972)
piCameraRate = 16



class Detection:
    def __init__(self,classify_server, confidence, model, params):
        self.confidence = confidence
        self.model = model
        self.video_url = params['url']
        self.hashes = {}
        self.topic_label = None
        self.net = classify_init() 
        self.video_s = None
        self.cam = str(params['id'])
        self.classify_server = classify_server
        self.errors = 0
        self.created_time = time.time() * 1000
        self.last_update_time = self.created_time
        self.idle_time = 0
        self.processes = []
        self.os = params['os']
        self._objects_counted = Value('i', 0)
        self.is_it_image = bool(re.search(image_check, self.video_url, re.IGNORECASE))                  
        self.is_it_simple_decode = bool(re.search(simple_decode, self.video_url, re.IGNORECASE))


    @classmethod
    def create(cls, classify_server, confidence, model, params):
        self = cls(classify_server, confidence, model, params)      
        return self

    '''    async def setup(self):
        # perform any necessary async setup here
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        tasks = [self.classify() for _ in range(NUMBER_OF_THREADS)]
        await asyncio.gather(*tasks)
    '''
    


    def classify(self):
        while True:
            frame = None
            try:
                logging.info("url: {} , is_it_image: {} is_it_simple_decode: {}, ".format(self.video_url, self.is_it_image, self.is_it_simple_decode))
                if self.is_it_simple_decode:
                    #print("#############4")           
                    frame = self.read_by_imdecode()
                    logging.info("frame was populated by self.read_by_imdecode for url: {}".format(self.video_url))
                elif self.is_it_image:                    
                    frame = imutils.url_to_image(self.video_url)
                    #print("#############3")
                    logging.info("frame was populated by imutils.url_to_image for url: {}".format(self.video_url))    
                else:
                    try:
                        if not self.video_s:
                            self.video_s = self.init_video_stream()
                            logging.debug("self.video_s initialised: {}".format(self.video_s))
                            self.video_s.set(cv2.CAP_PROP_BUFFERSIZE, 2)
                        frame = self.read_video_stream()
                        logging.debug("A frame was found by VideoStream() for: {}".format(self.video_url))
                    except cv2.error as e:
                        logging.critical("An error occurred: {}".format(e))
            except Exception as ex:
                logging.critical("Exception occurred when connected to URL: {}, {}".format(self.video_url, ex))
                self.errors += 1
            else:
                self.errors = 0
            if frame is not None: 
                #result = await asyncio.to_thread(self.call_classifier_locally, frame, self.cam, self.confidence, self.model)
                self.call_classifier_locally(frame, self.cam, self.confidence, self.model)
                '''
                if sys.version_info >= (3, 7):
                    # Use asyncio.to_thread if Python 3.7 or higher
                    result = await asyncio.to_thread(self.call_classifier_locally, frame, self.cam, self.confidence, self.model)
                else:
                    # Use a ThreadPoolExecutor for older versions of Python
                    result = await asyncio.get_event_loop().run_in_executor(executor, self.call_classifier_locally, frame, self.cam, self.confidence, self.model) 

                with self._objects_counted.get_lock(): 
                    self._objects_counted.value += result['objects_counted']
                '''    
            # Check if time threshold has passed
            current_time = time.time()*1000
            time_threshold = update_urls_from_stream_interval # Threshold in seconds
            if current_time - self.last_update_time >= time_threshold:
                record_locked = not self.update_urls_db()
                with self._objects_counted.get_lock(): 
                    self._objects_counted.value = -1 if self.errors >= URL_PINGS_NUMBER or self.idle_time > 28800 else 0 
                self.last_update_time = current_time
                idle = self.idle_time > 100 or self.errors >= URL_PINGS_NUMBER
                if(record_locked or idle ):
                    self.errors = 0
                    # consider if URL was not updated buy Detection process more then 2 intervals of processing time
                    videos = db.select_old_urls_which_not_mine_olderThen_secs(self.os,update_urls_from_stream_interval)
                    for video in videos:
                        self.video_url = video['url']
                        self.cam = str(video['id'])
                        self.idle_time = 0                           
                        self.created_time = time.time() * 1000 
                        self.is_it_image = bool(re.search(image_check, self.video_url, re.IGNORECASE))                  
                        self.is_it_simple_decode = self.video_url or bool(re.search(simple_decode, self.video_url, re.IGNORECASE))
                        if not ping_video_url(self.video_url):
                            with self._objects_counted.get_lock(): self._objects_counted.value = -1
                            self.update_urls_db()
                            continue 
                        elif not self.is_it_image and not self.is_it_simple_decode: 
                            self.video_s  = self.init_video_stream()                        
                        record_locked = not self.update_urls_db()
                        with self._objects_counted.get_lock(): self._objects_counted.value = 0
                        if record_locked: continue
                        else: break

                    
    def read_video_stream(self):
        if self.video_s is None:
            logging.debug("Start of initializing video stream by cv2 standard library \n for url {}".format(self.video_url))
            self.video_s = self.init_video_stream()
            logging.debug("video_s inititialised {}".format(self.video_s))
        if 'picam' == self.video_url:
            frame = self.video_s.read()
        else:
            try:        
                flag, frame = self.video_s.read()
                if not flag:
                    self.video_s.release()
                    #re-initialise and re-capture again:
                    if 'http' in self.video_url:
                        self.video_s = cv2.VideoCapture(self.video_url)
                    else:
                        self.video_s = VideoStream(src=int(self.video_url)).start()
                    flag, frame = self.video_s.read()
            except (cv2.error, ValueError) as e:
                logging.info("[ERROR] Cannot read video source {}. {}".format(self.video_url, str(e)))
                frame = None
        return frame                    

    def update_urls_db(self):
        params = {
            'last_time_updated': time.time() * 1000,
            'id': self.cam,
        }
        if self.topic_label is not None: params['desc'] = self.topic_label
        
        if( self._objects_counted.value <= 0 ):
            self.idle_time += (time.time() * 1000 - self.last_update_time) / 60000
            params['idle_in_mins'] = self.idle_time
        params['objects_counted'] = self._objects_counted.value
        try:
            db.update_urls(params)
        except Exception as e:
            logging.debug("More probably record locking exceptiion {}".format(e))
            return False;    
        logging.debug("URL {}, ID: {} updated with objects counted: {}".format(self.video_url, self.cam, self._objects_counted.value))
        return True
            
    def init_video_stream(self):
        video_s = None
        if 'picam' == self.video_url:
            video_s = VideoStream(usePiCamera=True, resolution=piCameraResolution, framerate=piCameraRate).start()
            time.sleep(2.0)
        else:
            try:
                if 'http' in self.video_url:                                       
                    video_s = cv2.VideoCapture(self.video_url)
                     # video_s.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                else:
                    video_s = VideoStream(src=int(self.video_url)).start()
            except cv2.error as e:
                logging.info("[ERROR] Cannot open video source {}: {}".format(self.video_url, e))
            except ValueError:
                logging.critical("[ERROR] Invalid video source: {}".format(self.video_url))
        return video_s

    def read_by_imdecode(self):
        response = requests.get(self.video_url, stream=True)
        if response.status_code == 200:
            content = bytes()
            for chunk in response.iter_content(chunk_size=4096):
                content += chunk
                a = content.find(b'\xff\xd8')
                b = content.find(b'\xff\xd9')
                if a != -1 and b != -1:
                    jpg = content[a:b+2]
                    content = content[b+2:]
                    frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

                    return frame
        else:
            raise ValueError("Failed to read frame from video stream")
        return None

    '''
    def read_by_imdecode(self):
        response = requests.get(self.video_url, stream=True)
        if response.status_code != 200:
            raise ValueError("Failed to read frame from video stream")
            
        # Iterate over response chunks and decode image frames
        for chunk in response.iter_content(chunk_size=1024):
            a = chunk.find(b'\xff\xd8')
            b = chunk.find(b'\xff\xd9')
            if a != -1 and b != -1:
                jpg = chunk[a:b+2]
                frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                return frame

        return None
    '''
   
    def call_classifier_locally(self, frame, cam, confidence, model):
        parameters = {'cam': cam, 'confidence': confidence , 'model': model, 'classes': ['person'] , 'topic_rules':  topic_rules} 
        logging.debug("------------ call_classifier (local) for cam: {} -------".format(cam))         
        result = classify_frame(frame, parameters, self.net)
        self.topic_label = result['topic_label']       
        if result['oject_images']:
            populate_db(result, cam)            
            logging.debug("... frame classified: {}".format(result))
        return result   

def populate_db(result, cam):
    now = datetime.datetime.now()
    day = "{date:%Y-%m-%d}".format(date=now)

    print(result)
    
    for object_label, cropped_images in result["oject_images"].items():
        for i in range(len(cropped_images)): 
            # Assuming `image` is a PIL Image object            
            object_image = np.asarray(cropped_images[i])
            #try to classify image one more time
            
            object_hash = result["object_hashes"][object_label][i]            
            object_coordinates = result["rectangles"][object_label][i]

        db.insert_frame(
            object_hash,
            day,
            int(time.time()*1000),
            object_label,
            object_image,
            object_coordinates['start_x'],
            object_coordinates['start_y'],
            object_coordinates['end_x'] - object_coordinates['start_x'],
            object_coordinates['end_y'] - object_coordinates['start_y'],
            cam
        )

    do_statistic(cam, result["object_hashes"],  result["counted_objects"])



def call_classifier(classify_server, frame, cam, confidence, model):
    
    _,im_bytes = cv2.imencode('.jpg', frame)
   
    parameters = {'cam': cam, 'confidence': confidence , 'model': model} 
   
    im_b64 = base64.b64encode(im_bytes).decode("utf8")
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}  
    payload = json.dumps({'image': im_b64, 'parameters': parameters}, indent=2)
    jsonResponse = None
    logging.debug("------------ call_classifier for cam: {} -------".format(cam))
    try:
        response = requests.post(url=classify_server,
                            data=payload, headers=headers)  
        #print("response is:"+ str(response) )                          
        response.raise_for_status()
        # access JSOn content
        jsonResponse = response.json()
        #print(jsonResponse)
        logging.debug("Entire JSON response")
        logging.debug(jsonResponse)

    except HTTPError as http_err:
        print('HTTP error occurred when connected to {0}: {1}'.format(classify_server, http_err))
    except Exception as err:
        print('Connection to {} failed: {}'.format(classify_server,err))
    logging.debug("call_classifier jsonResponse for cam: {} {}".format(cam,jsonResponse ))   
    return jsonResponse

