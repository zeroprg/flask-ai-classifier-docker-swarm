import numpy as np
import cv2

from PIL import Image
import time
import datetime
import json

from project import db
from  project.objCountByTimer import ObjCountByTimer
from  project.config import ProductionConfig as prod

# initialize the list of class labels MobileNet SSD was trained to
# detect, then generate a set of bounding box colors for each class
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]
LOOKED1 = {"person": []}

subject_of_interes = ["person"]
DNN_TARGET_MYRIAD = False

HASH_DELTA = 8  # how many bits difference between 2 hashcodes
DIMENSION_X = 300
DIMENSION_Y = 300
piCameraResolution = (640, 480)  # (1024,768) #(640,480)  #(1920,1080) #(1080,720) # (1296,972)
piCameraRate = 16

#SECRET_CODE = open("/run/secrets/secret_code", "r").read().strip()

# static variable
net = None

def classify_init():
    global net
# Read configuration parameters
    if( net is None ) : # Call it once
        proto = prod.args['prototxt']
        model = prod.args['model']
        print("Network parameters: " + proto + ", " + model)
        if(model.find('caffe')>0): 
            net = cv2.dnn.readNetFromCaffe(proto, model)
        else:
            print("provide only caffe model network")   
        # specify the target device as the Myriad processor on the NCS
        if "DNN_TARGET_MYRIAD" in prod.args:
            net.setPreferableTarget(cv2.dnn.DNN_TARGET_MYRIAD)
        else:
            net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
        print("Net was setuped: " + str(net)) 
            
    return net


hashes = {}

def classify_frame( frame, params, net=classify_init()):
    topic_label = 'No data'
    objects_counted = 0
    result = {}
    cam = params['cam']
    confidence = params['confidence']
    rectangles = []
    # print(" Classify frame ... --->")
    #_frame = cv2.resize(frame, (DIMENSION_X, DIMENSION_Y))
    # _frame = imutils.resize(frame,DIMENSION_X)
    blob = cv2.dnn.blobFromImage(frame, 0.007843,
                                    (DIMENSION_X, DIMENSION_Y), (127.5, 127.5, 127.5), True)
    # set the blob as input to our deep learning object
    # detector and obtain the detections
        # loop over the detections
    (fH, fW) = frame.shape[:2]
 
    net.setInput(blob)
    detections = net.forward()

    # logger.debug(detections)
    if detections is not None:
        # loop over the detections
        for i in np.arange(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated
            # with the prediction
            # filter out weak detections by ensuring the `confidence`
            # is greater than the minimum confidence
            if detections[0, 0, i, 2] < confidence:
                continue

            # otherwise, extract the index of the class label from
            # the `detections`, then compute the (x, y)-coordinates
            # of the bounding box for the object
            idx = int(detections[0, 0, i, 1])
            if idx > len(CLASSES) - 1:
                continue
            key = CLASSES[idx]

            if key not in LOOKED1:
                continue
            dims = np.array([fW, fH, fW, fH])
            box = detections[0, 0, i, 3:7] * dims
            (startX, startY, endX, endY) = box.astype("int")

            # draw the prediction on the frame
            if idx > len(CLASSES) - 1:
                continue
            key = CLASSES[idx]
            # if not key in IMAGES: continue
            # use 20 pixels from the top for labeling
            crop_img_data = frame[startY - 20:endY, startX:endX]
            # label = "Unknown"
            hash = 0
            try:
                crop_img = Image.fromarray(crop_img_data)
                hash = dhash(crop_img)
            except:
                continue  # pass

            if key not in LOOKED1:
                continue
            probability = detections[0, 0, i, 2] 
            label1 = "{}: {:.2f}%".format(key, int(probability * 100))
            # Draw rectangles

            #cv2.rectangle(frame, (startX - 25, startY - 25), (endX + 25, endY + 25), (255, 0, 0), 1)
            #cv2.putText(frame, label1, (startX - 25, startY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
            rectangle = {"startX": startX, "endX": endX, "startY": startY, "endY": endY, "text": label1}
            rectangles.append(rectangle)
            if hashes.get(key, None) is None:
                # count objects for last sec, last 5 sec and last minute

                hashes[key] = ImageHashCodesCountByTimer()
                if not hashes[key].add(hash):
                    continue

            else:
                # if not is_hash_the_same(hash,hashes[key]): hashes[key].add(hash)
                if not hashes[key].add(hash):
                    continue
                label = ''
                for key in hashes:
                    if hashes[key].getCountedObjects() == 0:
                        continue
                    label += ' ' + key + ':' + str(hashes[key].getCountedObjects())
                    result[key] = hashes[key].getCountedObjects()
                    objects_counted += result[key] 
                topic_label = label
                


            # process further only  if image is really different from other ones
            if key in subject_of_interes:
                x_dim = endX - startX
                y_dim = endY - startY
                #font_scale = min(y_dim, x_dim) / 300
                #if font_scale > 0.12:
                #    cv2.putText(crop_img_data, str(datetime.datetime.now().strftime('%H:%M %d/%m/%y')), (1, 15),
                #                cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 0), 1)

                now = datetime.datetime.now()
                day = "{date:%Y-%m-%d}".format(date=now)
                db.insert_frame( hash, day, int(time.time()*1000), key, crop_img_data, startX, startY, x_dim, y_dim, cam)
                
            do_statistic(cam,  hashes)
            #db.getConn().commit()

        # draw at the top left corner of the screen
        #cv2.putText(frame, topic_label, (10, 23), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        # print(" Classify frame ... <---")
        # place frame in queue for further processing
        result["topic_label"] = topic_label
        result["rectangles"] = rectangles
        result["objects_counted"] = objects_counted
    return result #frame



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
    resized = cv2.resize(image, (hashSize, hashSize), interpolation=cv2.INTER_LINEAR)
    diff = resized[:, 1:] > resized[:, :-1]
    # convert the difference image to a hash
    return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])
