
import numpy as np
import YOLO_classifier, Cafe_classifier

class Classifier:
    def __init__(self, model):
        self.model = model

    def classify(self, frame, params):
        if self.model == 'yolov4':
            net = YOLO_classifier()
        elif self.model == 'caffe':
            net = Cafe_classifier()

        result = net.classify_frame(frame, params)
        return result