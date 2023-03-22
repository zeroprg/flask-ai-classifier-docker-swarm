import cv2
import numpy as np
import NeuralNetwork

class YOLOModel(NeuralNetwork):
    
    def __init__(self, model_path, weights_path, conf_thresh=0.5, nms_thresh=0.5, input_size=None):
        self.net = cv2.dnn.readNetFromDarknet(model_path, weights_path)
        self.conf_thresh = conf_thresh
        self.nms_thresh = nms_thresh
        self.input_size = input_size or (416, 416)
        
    @staticmethod
    def read_yolo_class_file(class_file):
        class_dict = {}
        with open(class_file, 'r') as f:
            classes = f.read().splitlines()

        for i, cls in enumerate(classes):
            class_dict[cls] = i
        return class_dict


    def predict(self, input_data):
        blob = cv2.dnn.blobFromImage(input_data, 1/255, self.input_size, swapRB=True, crop=False)
        self.net.setInput(blob)
        layer_names = self.net.getLayerNames()
        output_names = [layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        outputs = self.net.forward(output_names)
        detections = []
        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > self.conf_thresh:
                    center_x = int(detection[0] * input_data.shape[1])
                    center_y = int(detection[1] * input_data.shape[0])
                    width = int(detection[2] * input_data.shape[1])
                    height = int(detection[3] * input_data.shape[0])
                    left = int(center_x - width / 2)
                    top = int(center_y - height / 2)
                    detections.append([left, top, width, height, confidence, class_id])
        if len(detections) > 0:
            detections = np.array(detections)
            boxes = detections[:, :4].astype(np.int32)
            scores = detections[:, 4].astype(np.float32)
            class_ids = detections[:, 5].astype(np.int32)
            indices = cv2.dnn.NMSBoxes(boxes, scores, self.conf_thresh, self.nms_thresh)
            detections = detections[indices.flatten()] if len(indices) > 0 else []
        return detections