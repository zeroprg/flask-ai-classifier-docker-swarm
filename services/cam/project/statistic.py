import cv2
import time
import json
import numpy as np
import time
import hashlib

#import project.ObjCountByTimer

from project import db


HASH_DELTA = 6  # bigger number  more less difference between objects

def do_statistic(cam, hashes, counted_objects):
    # Do some statistic work here    
    params = parameterise_json(cam, hashes, counted_objects )
    db.insert_statistic(params)
    return params

def parameterise_json( cam, hashes, counted_objects):
    #print( counted_objects )
    ret = []
    for key in hashes:
        # logging.debug(images[key])
        trace = Trace()
        trace.name = key
        trace.cam = cam       
        tm = int(time.time()*1000)  # strftime("%H:%M:%S", localtime())
        trace.hashcodes = [str(x) for x in hashes[key]]
        trace.x = tm
        # last = len(hashes[key].counted) -1
        trace.y = counted_objects[key]
        # trace.text = str(trace.y) + ' ' + key + '(s)'
        ret.append(trace.__dict__)  # used for proper JSON generation (dictionary)
        # ret.append(trace)
        #print( trace.__dict__ )
    return ret

class ImageHashCodesCountByTimer():
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

def get_parameters_json(hashes, cam):
    ret = []
    for key in hashes:
        # logging.debug(images[key])
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




def dhash(image_data, hashSize=8):
    image_out = np.array(image_data).astype(np.uint8)

    # convert the image to grayscale and compute the hash
    image = cv2.cvtColor(image_out, cv2.COLOR_BGR2GRAY)

    # resize the input image, adding a single column (width) so we
    # can compute the horizontal gradient
    resized = cv2.resize(image, (hashSize + 1, hashSize), interpolation=cv2.INTER_LINEAR)

    # compute the horizontal gradient between adjacent columns
    diff = resized[:, 1:] > resized[:, :-1]

    # convert the difference image to a hash
    return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])

def hash_image(image):
    # Convert the image to a bytes object
    # Assuming cropped_image is a numpy array
    #image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #print("image: {}".format(image))
    # Assuming `image` is a PIL Image object
    image_np = np.asarray(image)
    img_bytes = cv2.imencode('.png', image_np)[1].tobytes()

    # Compute the SHA-256 hash of the bytes object
    hash_bytes = hashlib.sha256(img_bytes).digest()

    # Return the first 8 bytes of the hash as a bytes object
    return hash_bytes[:8]