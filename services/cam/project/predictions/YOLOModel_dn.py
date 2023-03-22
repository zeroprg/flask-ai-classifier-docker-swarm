import cv2
import numpy as np
import darknet as dn
import NeuralNetwork

class YOLO(NeuralNetwork):
    def __init__(self, model_path, weights_path, input_size=None):
        #dn.set_gpu(0) use it if you have GPU
        self.net = dn.load_net(str.encode(model_path), str.encode(weights_path), 0)
        self.meta = dn.load_meta(str.encode(model_path.replace('.cfg', '.data')))
        self.input_size = input_size or (dn.network_width(self.net), dn.network_height(self.net))

    @staticmethod
    def read_yolo_class_file(class_file):
        class_dict = {}
        with open(class_file, 'r') as f:
            classes = f.read().splitlines()

        for i, cls in enumerate(classes):
            class_dict[cls] = i
        return class_dict
    
    def predict(self, input_data, detection_classes=None, confidence_thresh=0.5):
        input_data = cv2.resize(input_data, self.input_size)
        detections = dn.detect(self.net, self.meta, input_data, thresh=confidence_thresh)
        if detection_classes is not None:
            detections = [d for d in detections if d[0] in detection_classes]
        return detections