import cv2
import numpy as np

import ClassifyInterface

class CaffeClassifier(ClassifyInterface):
    def __init__(self, prototxt, model, mean, confidence_threshold, DNN_TARGET_MYRIAD=True):
        self.net = cv2.dnn.readNetFromCaffe(prototxt, model)
        if DNN_TARGET_MYRIAD: 
             self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_MYRIAD)
        self.mean = mean
        self.confidence_threshold = confidence_threshold
    
    def classify(self, image):
        # Pre-process the input image
        (height, width) = image.shape[:2]
        blob = cv2.dnn.blobFromImage(image, 0.007843, (width, height), (127.5, 127.5, 127.5), swapRB=True)

        self.net.setInput(blob)
        detections = self.net.forward()

        objects = []
        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            if confidence > self.confidence_threshold:
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
                (start_x, start_y, end_x, end_y) = box.astype("int")

                objects.append((idx, confidence, (start_x, start_y, end_x, end_y)))
        
        return objects
