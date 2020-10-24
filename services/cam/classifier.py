import numpy as np
from imutils.video import VideoStream


import dhash
from PIL import Image
import time
import datetime
import json
from objCountByTimer import ObjCountByTimer
from multiprocessing import Process
from multiprocessing import Queue

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
    def __init__(self, sqlite_db,ipaddress, confidence, prototxt, model, video_url, output_queue, cam):
        self.confidence = confidence
        self.prototxt = prototxt
        self.model = model
        self.video_url = video_url
        self.hashes = {}
        self.sqlite_db = sqlite_db
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
                frame = self.read_video_stream(self.video_s)
                if frame is None:
                    return
            except:
                return
            frame = self.classify_frame(self.net, frame, cam)
            output_queue.put_nowait(frame)

    def init_video_stream(self):
        video_s = VideoStream(self.video_url,usePiCamera=('picam' == self.video_url), resolution=piCameraResolution,
                      framerate=piCameraRate).start()
        time.sleep(2.0)
        return video_s

    def read_video_stream(self, video_s):
        # print("Read video stream .. " + self.video_url)
        if 'picam' == self.video_url:
            frame = video_s.read()
        else:
            flag, frame = video_s.read()
            if not flag:
                video_s = VideoStream(self.video_url,usePiCamera=('picam' == self.video_url), resolution=piCameraResolution,
                      framerate=piCameraRate).start()
                flag, frame = video_s.read()
                return frame
        return frame





