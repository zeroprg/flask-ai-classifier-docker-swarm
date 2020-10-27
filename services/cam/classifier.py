import numpy as np
from imutils.video import VideoStream
import io
import zlib
import requests
from requests.exceptions import HTTPError

import dhash
from PIL import Image
import time
import datetime
import json
from objCountByTimer import ObjCountByTimer
from multiprocessing import Process
from multiprocessing import Queue

CLASSIFIER_SERVER = 'http://192.168.0.167/classify'

# initialize the list of class labels MobileNet SSD was trained to
# detect, then generate a set of bounding box colors for each class
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]
LOOKED1 = {"person": [], "car": []}

subject_of_interes = ["person", "car"]
DNN_TARGET_MYRIAD = False

HASH_DELTA = 43  # bigger number  more precise object's count
DIMENSION_X = 300
DIMENSION_Y = 300
piCameraResolution = (640, 480)  # (1024,768) #(640,480)  #(1920,1080) #(1080,720) # (1296,972)
piCameraRate = 16
NUMBER_OF_THREADS = 1

class Detection:
    def __init__(self, ipaddress, confidence, prototxt, model, video_url, output_queue, cam):
        self.confidence = confidence
        self.prototxt = prototxt
        self.model = model
        self.video_url = video_url
        self.hashes = {}
        self.db_ipaddress = ipaddress
        self.topic_label = 'no data'
        self.net = self.video_s = None

        for i in range(NUMBER_OF_THREADS):
            p_get_frame = Process(target=self.classify,
                                  args=(output_queue, cam))
            p_get_frame.daemon = True
            p_get_frame.start()
            time.sleep(0.1 + 0.99/NUMBER_OF_THREADS)

    def classify(self, output_queue, cam):
        if self.video_s is None:
            self.video_s = self.init_video_stream()
        while True:
            try:
                frame = self.video_s.read()
                if frame is None: continue
            except:
                print('Exception during reading stream by URL:{0}'.format(self.video_s))
                return
            result = call_classifier(frame, cam, self.confidence)
            print("cam {0} result: {1}".format(cam, result))

            #output_queue.put_nowait(frame)


    def init_video_stream(self):
        #logger.info(self.video_url, ('picam' == self.video_url))
        video_s = VideoStream(self.video_url,usePiCamera=('picam' == self.video_url), resolution=piCameraResolution,
                      framerate=piCameraRate).start()
        #logger.info(video)
        time.sleep(2.0)
        return video_s





def call_classifier(frame, cam, confidence):
    data = frame.tolist()  #, _ , _ = compress_nparr(frame)
    parameters = {'cam': cam, 'confidence': confidence}
    data = {'params': parameters, 'array':data}
    jsonResponse = None
    try:
        response = requests.post(url=CLASSIFIER_SERVER,
                            json=data)
#                            headers={'Content-Type': 'text/json'})
        response.raise_for_status()
        # access JSOn content
        jsonResponse = response.json()
        print("Entire JSON response")
        print(jsonResponse)

    except HTTPError as http_err:
        print('HTTP error occurred: {0}'.format(http_err))
    except Exception as err:
        print('Other error occurred: {0}')#.format(err))
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
