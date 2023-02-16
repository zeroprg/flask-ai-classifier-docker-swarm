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
from multiprocessing import Process,Value

import json

from project import db
from project.caffe_classifier import classify_frame
from project import URL_PINGS_NUMBER, NUMBER_OF_THREADS, update_urls_from_stream_interval
subject_of_interes = ["person", "car"]
DNN_TARGET_MYRIAD = False

HASH_DELTA = 70  # bigger number  more precise object's count
DIMENSION_X = 300
DIMENSION_Y = 300
piCameraResolution = (640, 480)  # (1024,768) #(640,480)  #(1920,1080) #(1080,720) # (1296,972)
piCameraRate = 16

logging.basicConfig(level=logging.INFO)

class Detection:
    def __init__(self, classify_server, confidence, model, video):
        self.confidence = confidence
        self.model = model
        #self.video_url = f"{video['url']}{'?' if '?' not in video['url'] else '&'}stream=full&needlength"
        self.video_url = video['url']
        self.hashes = {}
        self.topic_label = 'no data'
        self.net = self.video_s = None
        self.cam = video['id']
        self.classify_server = classify_server
        self.errors = 0
        self.created_time = time.time() * 1000
        self.last_update_time = self.created_time
        self.idle_time = 0
        self.processes = []
        self._objects_counted = Value('i', 0)
        self.frame_counter = 0
        

        for _ in range(NUMBER_OF_THREADS):
            p_get_frame = Process(target=self.classify)
            p_get_frame.start()
            self.processes.append(p_get_frame)
            logging.info("Process started for video: {}".format(video))
            time.sleep(0.1 + 0.69 / NUMBER_OF_THREADS)

    def classify(self):
        if self.video_s is None:
            self.video_s = self.init_video_stream()
        while True:
            try:
                if re.search(r'\.jpg|\.gif|\.png', self.video_url):
                    frame = imutils.url_to_image(self.video_url)
                else:
                    frame = self.read_video_stream(self.video_s)
                if frame is None:
                    self.errors += 1
                    return False
            except Exception as ex:
                logging.critical("Exception occurred when connected to URL: {}, {}".format(self.video_url,ex))
                self.errors += 1
                return False
            else:
                self.errors = 0
            result = call_classifier_locally(self, frame, self.cam, self.confidence, self.model)
            with self._objects_counted.get_lock():
                self._objects_counted.value += result['objects_counted']
            self.frame_counter += 1
                    # Check if time threshold has passed
            current_time = time.time()*1000
            time_threshold = update_urls_from_stream_interval # Threshold in seconds
            if current_time - self.last_update_time >= time_threshold:
                self.errors = 0
                self.update_urls_db()
                self.last_update_time = time.time() * 1000
            if self.errors > URL_PINGS_NUMBER:
                for process in self.processes:
                    process.terminate()
                return False

    def update_urls_db(self):
        params = {
            'last_time_updated': time.time() * 1000,
            'id': self.cam,
        }
        if self._objects_counted.value == 0 or self.errors > URL_PINGS_NUMBER:
            self.idle_time += (time.time() * 1000 - self.last_update_time) / 60000
            params['idle_in_mins'] = self.idle_time
        params['objects_counted'] = self._objects_counted.value
        db.update_urls(params)
        logging.debug("URL {}, ID: {} updated with objects counted: {}".format(self.video_url, self.cam, self._objects_counted.value))

    def init_video_stream(self):
        video_s = None
        if 'picam' == self.video_url:
            video_s = VideoStream(usePiCamera=True, resolution=piCameraResolution, framerate=piCameraRate).start()
            time.sleep(2.0)
        else:
            try:
                if 'http' in self.video_url:
                    video_s = VideoStream(src=self.video_url).start()
                else:
                    video_s = VideoStream(src=int(self.video_url)).start()
            except:
                print("[ERROR] Cannot open video source {}".format(self.video_url)
)
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
        print('Connection to {0} failed: {1}'.format(classify_server,err))
    logging.debug("call_classifier jsonResponse for cam: {} {}".format(cam,jsonResponse ))   
    return jsonResponse

