import numpy as np
import cv2

from PIL import Image
import math

from project.config import ProductionConfig as prod
from project.statistic import dhash


# initialize the list of class labels MobileNet SSD was trained to
# detect, then generate a set of bounding box colors for each class

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow",
           "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train",
           "tvmonitor", "cellphone", "backpack", "umbrella", "book", "traffic light", "stop sign", "fire hydrant",
           "parking meter", "bench", "flower", "tree", "building", "elephant", "bear", "zebra", "giraffe",
           "pizza", "donut", "cake", "couch", "bed", "table", "toilet", "sink", "oven", "microwave", "refrigerator",
           "blender", "toaster", "scissors", "teddy bear", "hair drier", "toothbrush"]


DNN_TARGET_MYRIAD = False

HASH_DELTA = 8  # how many bits difference between 2 hashcodes
DIMENSION_X = 300
DIMENSION_Y = 300

# static variable

proto = None
model = None
confidence = None
fH = None
fW = None
dims = None
net_target = None

def read_configuration():
    global proto, model, confidence, net_target
    proto = prod.args['prototxt']
    model = prod.args['model']
    print("Network parameters: " + proto + ", " + model)
    if model.find('caffe') > 0:
        net_target = cv2.dnn.DNN_TARGET_CPU
    else:
        print("provide only caffe model network")
    # specify the target device as the Myriad processor on the NCS
    if "DNN_TARGET_MYRIAD" in prod.args:
        net_target = cv2.dnn.DNN_TARGET_MYRIAD
    confidence = prod.args.get('confidence', 0.5)

def classify_init():   
    read_configuration()

    net = cv2.dnn.readNetFromCaffe(proto, model)
    net.setPreferableTarget(net_target)
    print("Net was setuped: " + str(net))
    return net

hashes = {}

def process_detections(detections, frame, fW, fH, looked_for_classes, confidence):
    rectangles = {}
    counted_objects = {}
    cropped_images = {}

    for i in range(detections.shape[2]):
        confidence_score = detections[0, 0, i, 2]

        if confidence_score >= confidence:
            class_index = int(detections[0, 0, i, 1])
            
            if math.isnan(class_index):
                continue

            class_name = CLASSES[class_index]

            #if class_name not in looked_for_classes:
            #    continue

            dims = np.array([fW, fH, fW, fH])
            box = detections[0, 0, i, 3:7] * dims
            (start_x, start_y, end_x, end_y) = box.astype("int")


                        
            if class_name in looked_for_classes:
                if start_x < 0 or end_x < 0 or start_y < 20 or end_y < 0:
                    continue
                print("class_name: {}, class_index: {}".format(class_name, class_index))

                crop_img_data = frame[start_y - 20:end_y, start_x:end_x]
                crop_img = Image.fromarray(crop_img_data)

                rectangle = {"start_x": start_x, "end_x": end_x, "start_y": start_y, "end_y": end_y, "text": "{}: {:.2f}%".format(class_name, confidence_score * 100)}
                if class_name not in rectangles:
                    rectangles[class_name] = []
                rectangles[class_name].append(rectangle)
                if class_name not in counted_objects:
                    cropped_images[class_name] = [crop_img]
                else:
                    cropped_images[class_name].append(crop_img)


            if class_name not in counted_objects:
                counted_objects[class_name] = 1
            else:
                counted_objects[class_name] += 1

    return rectangles, counted_objects, cropped_images

def classify_topic(object_labels, topic_rules):
    """
    Classify the topic based on the detected objects using a set of topic rules.

    Args:
    - object_labels: a list of labels of detected objects.
    - topic_rules: a dictionary of topic rules, with the key being the topic name and the value being a tuple of the form
      (list of object labels that belong to that topic, minimum number of objects required to match the topic rule).

    Returns:
    - topic_label: the label of the topic that the detected objects belong to.
    """

    # initialize the topic label and maximum number of matched objects as None
    topic_label = None
    max_matched_objects = 0

    # loop through the topic rules
    for topic, (rule, min_objects) in topic_rules.items():
        # check if the minimum number of objects required to match the rule is less than or equal to the number of detected objects
        if min_objects <= len(object_labels):
            # check if all the object labels in the rule are in the detected object labels
            matched_objects = sum(1 for label in rule if label in object_labels)
            if matched_objects >= min_objects and matched_objects > max_matched_objects:
                topic_label = topic
                max_matched_objects = matched_objects

    return topic_label



def classify_frame(frame, params, net=classify_init()):
    # preprocess the frame 
    blob = cv2.dnn.blobFromImage(frame, 0.007843,
                                    (DIMENSION_X, DIMENSION_Y), (127.5, 127.5, 127.5), True)
    # set the blob as input to our deep learning object
    # detector and obtain the detections
        # loop over the detections
    (fH, fW) = frame.shape[:2]


    # set the input to the neural network and perform a forward pass
    net.setInput(blob)
    detections = net.forward()
    # process the detections and count objects
    looked_for_classes = params['classes']
    confidence = params['confidence']
    rectangles, counted_objects, cropped_images = process_detections(detections, frame, fW, fH, looked_for_classes, confidence)

    object_hashes = {}
    for class_name, cropped_images_ in cropped_images.items():
        # Assuming cropped_images is an array of images
        object_hashes[class_name] = []
        for cropped_image in cropped_images_:
            object_hash = dhash(cropped_image)
            object_hashes[class_name].append(object_hash)


    
    result = {}

    result["rectangles"] = rectangles
    result["counted_objects"] = counted_objects
    result["object_hashes"] = object_hashes

    # label the frame based on the detected objects
    result["objects_labels"] = list(counted_objects.keys())
    topic_label = classify_topic(result["objects_labels"], params['topic_rules'])
    if topic_label is not None: print(topic_label)
    result["topic_label"] = topic_label  
    result["oject_images"] = cropped_images
  
    return result


