import cv2
import numpy as np
import imutils
from imutils.video import VideoStream
import io
import zlib
import requests
from requests.exceptions import HTTPError

import re
import logging
import base64
import time
import json
from multiprocessing import Process

import json

from json import JSONEncoder
from project import db
from project.caffe_classifier import classify_frame
from project import update_urls_from_stream_interval, URL_PINGS_NUMBER
subject_of_interes = ["person", "car"]
DNN_TARGET_MYRIAD = False

HASH_DELTA = 70  # bigger number  more precise object's count
DIMENSION_X = 300
DIMENSION_Y = 300
piCameraResolution = (640, 480)  # (1024,768) #(640,480)  #(1920,1080) #(1080,720) # (1296,972)
piCameraRate = 16
NUMBER_OF_THREADS = 1


logging.basicConfig(level=logging.INFO)


class Detection:

    def __init__(self, classify_server, confidence, model, video):

        self.confidence = confidence
        self.model = model
        self.video_url = video['url'] #+ '?' if '?' not in  video['url'] else '&' + 'stream=full&needlength'
        self.hashes = {}        
        self.topic_label = 'no data'
        self.net = self.video_s = None
        self.cam = video['id']
        self.classify_server = classify_server
        self.errors = 0
        self.createdtime = time.time()*1000
        self.processes = []
        self._objects_counted = 0
        self.frame_counter = 0
    
        

        for i in range(NUMBER_OF_THREADS):
            p_get_frame = Process(target=self.classify)

                                  #,output_queue))
            p_get_frame.daemon = False
            self.processes.append(p_get_frame)
            p_get_frame.start()
            logging.info("-------- Process was just started for video: {} --------".format(video))
            time.sleep(0.1 + 0.69/NUMBER_OF_THREADS)
            

    @property
    def objects_counted(self):
        return self._objects_counted   
    
    @objects_counted.setter
    def objects_counted(self, value):
        self._objects_counted = value


    def classify(self):
        global objects_counted
        if self.video_s is None:
            self.video_s = self.init_video_stream()
        while True:
            try:                
                if re.search('\.jpg|\.gif|\.png', self.video_url):
                    #logging.debug("Try to connect jpg static {} ".format(self.video_url))
                    frame = imutils.url_to_image(self.video_url)
                   # logging.debug("Connection to jpg static {} successed ".format(self.video_url))
                else:
                   # logging.debug("Try to connect to video {} ".format(self.video_url))
                    frame = self.read_video_stream(self.video_s)
                    
                  #  logging.debug("Connection to video {} successed ".format(self.video_url))
                if frame is None: return False
            except:
                logging.critical('Exception when connected to URL:{0}'.format(self.video_url))
                self.errors += 1 
                return False
            else:
                self.errors = 0
            # call it remotely
            #result = call_classifier(self.classify_server, frame, self.cam, self.confidence, self.model)
            # call locally
            result = call_classifier_locally(self,  frame, self.cam, self.confidence, self.model)            
            self._objects_counted = self._objects_counted + result['objects_counted'] # doesn't work , always 0
            self.frame_counter += 1            
            if( self.frame_counter  > 1000 ): 
                self.frame_counter = 0
                self.update_urls_db()                 
                     
            if( self.errors > URL_PINGS_NUMBER):
                for process in self.processes: 
                    process.terminate()
                return False

                
            # Draw rectangles
            '''
            for rec in result['rectangles']:
                x = rec.get('startX') - 25
                y = rec.get('startY') - 25
                cv2.rectangle(frame, (x,y), (rec.get('endX') + 25, rec.get('endY') + 25), (255, 0, 0), 1)
                cv2.putText(frame, rec.get('text') , (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                cv2.putText(frame, result.get('topic_label', 'None')  , (10, 23), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        
        self.output_queue.put(frame)
        '''
            #output_queue.put_nowait(frame)
            
    """ Delete all detectors which have errors with connections """
    def update_urls_db(self):  
        # remove this  processes which older then 1 min and not pingable ( more then URL_PINGS_NUMBER pinged )
        params = {'last_time_updated': time.time()*1000, "id": self.cam}
        if( self.errors > URL_PINGS_NUMBER):
            params['idle_in_mins'] =  (time.time()*1000 - self.createdtime) / 60000
        params['objects_counted'] = self._objects_counted
        #self._objects_counted = 0
        db.update_urls(params) #do not delete url only update status how many minutess was not active. (time.time()*1000 - detectors[cam].createdtime)/1000
        logging.debug("Url {} . id :{} has been updated with objects_counted:{}".format(self.video_url, self.cam, self._objects_counted))
  

    def init_video_stream(self):
        video_s = None
        if 'picam' == self.video_url:
            video_s = VideoStream(usePiCamera=True, resolution=piCameraResolution, framerate=piCameraRate).start()
            time.sleep(2.0)

        else:
            # grab the frame from the threaded video stream
            try:
                if re.search('\.jpg|\.gif|\.png', self.video_url):
                    logging.debug("Try to connect jpg to {} ".format(self.video_url))
                    imutils.url_to_image(self.video_url)
                else:
      
                    logging.debug("Try to connect to video {} ".format(self.video_url))
                    video_s = cv2.VideoCapture(self.video_url)                    
                 
            except Exception as ex:
                self.errors += 1                    
                logging.critical('Error occurred when connected to {0}: {1}'.format(self.video_url, ex))
        logging.debug("self.errors: {}".format(self.errors))       
        
        return video_s

    def read_video_stream(self, video_s):
        # print("Read video stream .. " + self.video_url) 
        if 'picam' == self.video_url:
            frame = video_s.read()
        else:
            flag, frame = video_s.read()
            if not flag:
                video_s = cv2.VideoCapture(self.video_url)
                flag, frame = video_s.read()
                return frame
        return frame

def call_classifier_locally(self, frame, cam, confidence, model):
    parameters = {'cam': cam, 'confidence': confidence , 'model': model} 
    logging.debug("------------ call_classifier (local) for cam: {} -------".format(cam))
    result = classify_frame(frame, parameters)
    self.topic_label = result['topic_label'] if 'topic_label' in result else 'no data'
    logging.debug("... frame classified: {}".format(result))
    return result   


def call_classifier(classify_server, frame, cam, confidence, model):
    _,im_bytes = cv2.imencode('.jpg', frame) # frame.tolist() #  , _ , _ = compress_nparr(frame)
   
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
        print('Connection to {0} failed: {1}'.format(classify_server,err))
    logging.debug("call_classifier jsonResponse for cam: {} {}".format(cam,jsonResponse ))   
    return jsonResponse




def compress_nparr(nparr):
    """
    Returns the given numpy array as compressed bytestring,
    the uncompressed and the compressed byte size.
    """
    bytestream = io.BytesIO()
    np.save(bytestream, nparr)
    uncompressed = bytestream.getvalue()
    compressed = zlib.compress(uncompressed)
    return compressed, len(uncompressed), len(compressed)

    
def uncompress_nparr(bytestring):
    """  Uncompress as bytestring into numpy array  """
    return np.load(io.BytesIO(zlib.decompress(bytestring)))

    #resp, _, _ = compress_nparr(data10)
    #return Response(response=resp, status=200,
    #                mimetype="application/octet_stream")

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)