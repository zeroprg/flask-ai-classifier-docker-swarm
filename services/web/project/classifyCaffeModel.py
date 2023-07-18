from PIL import Image
import time
import datetime
import json
import logging

from project import db
from  project.tools.objCountByTimer import ObjCountByTimer
from  project.config import ProductionConfig as prod

logging.basicConfig(level=logging.INFO)

# initialize the list of class labels MobileNet SSD was trained to
# detect, then generate a set of bounding box colors for each class
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]
LOOKED1 = {"person": []}

subject_of_interes = ["person"]
DNN_TARGET_MYRIAD = False

HASH_DELTA = 7  # how many bits difference between 2 hashcodes
DIMENSION_X = 300
DIMENSION_Y = 300
piCameraResolution = (640, 480)  # (1024,768) #(640,480)  #(1920,1080) #(1080,720) # (1296,972)
piCameraRate = 16
NUMBER_OF_THREADS = 1


#SECRET_CODE = open("/run/secrets/secret_code", "r").read().strip()

# static variable

hashes = {}




class ImageHashCodesCountByTimer(ObjCountByTimer):
    def bitdiff(self, a, b):
        d = a ^ b
        return self.countSetBits(d)

    def countSetBits(self, n):
        count =0
        while(n):
            count += n&1
            n >>=1
        return count

    def equals(self, hash1, hash2):
        delta = self.bitdiff(hash1, hash2)
        return delta < HASH_DELTA


def do_statistic(cam, hashes):
    # Do some statistic work here
    params = get_parameters_json(hashes, cam)
    db.insert_statistic(params)
    return params


def get_parameters_json(hashes, cam):
    ret = []
    for key in hashes:
        trace = Trace()
        trace.name = key.split()[0]
        trace.cam = cam       
        tm = int(time.time()*1000)  # strftime("%H:%M:%S", localtime())
        trace.hashcodes = hashes[key].toString()
        trace.x = tm
        # last = len(hashes[key].counted) -1
        trace.y = hashes[key].getCountedObjects()
        # trace.text = str(trace.y) + ' ' + key + '(s)'
        ret.append(trace.__dict__)  # used for proper JSON generation (dictionary)
        # ret.append(trace)
        # logging.debug( trace.__dict__ )
    return ret


class Trace(dict):
    def __init__(self):
        dict.__init__(self)
        self.cam = ''
        self.x = 0
        self.y = 0
        self.name = ''
        self.text = ''
        self.filenames = []

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)