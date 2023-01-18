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

from project.caffe_classifier import classify_frame

subject_of_interes = ["person", "car"]
DNN_TARGET_MYRIAD = False

HASH_DELTA = 43  # bigger number  more precise object's count
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
        #self.output_queue = queue

        self.video_s = self.init_video_stream()


        

    def classify(self):

        while True:
            try:                
                if re.search('.jpg|.gif|.png', self.video_url):
                    frame = imutils.url_to_image(self.video_url)
                else:
                    frame = self.read_video_stream(self.video_s)
                if frame is None: return
            except:
                print('Exception during reading stream by URL:{0}'.format(self.video_url))
                return
            # call it remotely
            #result = call_classifier(self.classify_server, frame, self.cam, self.confidence, self.model)
            # call locally
            result = call_classifier_locally( frame, self.cam, self.confidence, self.model) 
            if(result is not None and 'rectangles' in result and len(result['rectangles'])>0):
                logging.debug("result: {}".format(result))

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
            

    def init_video_stream(self):
        video_s = None
        if 'picam' == self.video_url:
            video_s = VideoStream(usePiCamera=True, resolution=piCameraResolution, framerate=piCameraRate).start()
            time.sleep(2.0)

        else:
            # grab the frame from the threaded video stream
            try:
                video_s = cv2.VideoCapture(self.video_url)
                frame = self.read_video_stream(video_s)               
                
            except Exception as ex:
                self.errors += 1                    
                print('Error occurred when connected to {0}: {1}'.format(self.video_url, ex))
        if self.errors == 0: 
          for i in range(NUMBER_OF_THREADS):
            p_get_frame = Process(target=self.classify)

                                #,output_queue))
            p_get_frame.daemon = False
            p_get_frame.start()
            logging.info("-------- Process was just started for video: {} --------".format(self.video_url))
            time.sleep(0.1 + 0.69/NUMBER_OF_THREADS)
        
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

def call_classifier_locally( frame, cam, confidence, model):
       parameters = {'cam': cam, 'confidence': confidence , 'model': model} 
       classify_frame(frame, parameters)


def call_classifier(classify_server, frame, cam, confidence, model):
    _,im_bytes = cv2.imencode('.jpg', frame) # frame.tolist() #  , _ , _ = compress_nparr(frame)
   
    parameters = {'cam': cam, 'confidence': confidence , 'model': model} 
   
    im_b64 = base64.b64encode(im_bytes).decode("utf8")
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}  
    payload = json.dumps({'image': im_b64, 'parameters': parameters}, indent=2)
    jsonResponse = None
    logging.debug("------------ call_classifier just called for cam: {} -------".format(cam))
    try:
        response = requests.post(url=classify_server,
                            data=payload, headers=headers)  
        #print("response is:"+ str(response) )                          
        response.raise_for_status()
        # access JSOn content
        jsonResponse = response.json()
        print(jsonResponse)
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