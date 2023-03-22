import cv2
import numpy as np
import caffe
import NeuralNetwork


class CaffeModel(NeuralNetwork):
    def __init__(self, model_path, weights_path, input_size=None):
        self.net = caffe.Net(model_path, weights_path, caffe.TEST)
        self.input_size = input_size or (self.net.blobs['data'].shape[2], self.net.blobs['data'].shape[3])

    @staticmethod
    def read_caffe_prototxt(proto_file):
        with open(proto_file, 'r') as f:
            proto_txt = f.read()

        # Find the number of classes in the output layer
        class_index_start = proto_txt.find("num_classes:") + len("num_classes:")
        class_index_end = proto_txt.find("\n", class_index_start)
        num_classes = int(proto_txt[class_index_start:class_index_end].strip())

        # Find the name of each class in the output layer
        class_names_start = proto_txt.find("name: \"")
        class_names_end = proto_txt.find("\"", class_names_start + len("name: \""))
        class_names = []
        while class_names_start != -1:
            class_names.append(proto_txt[class_names_start+len("name: \""):class_names_end])
            class_names_start = proto_txt.find("name: \"", class_names_end)
            class_names_end = proto_txt.find("\"", class_names_start + len("name: \""))

        # Create a dictionary mapping each class name to its index
        class_dict = {name: index for index, name in enumerate(class_names)}

        return class_dict, num_classes

    def predict(self, input_data, detection_classes=None, confidence_thresh=0.5):
        input_data = cv2.resize(input_data, self.input_size)
        input_data = input_data.transpose((2, 0, 1))
        input_data = np.array([input_data])
        self.net.blobs['data'].data[...] = input_data
        output = self.net.forward()
        detections = []
        for i in range(output['detection_out'][0].shape[0]):
            confidence = output['detection_out'][0][i][2]
            class_id = int(output['detection_out'][0][i][1])
            if detection_classes is None or class_id in detection_classes and confidence > confidence_thresh:
                left = int(output['detection_out'][0][i][3] * input_data.shape[3])
                top = int(output['detection_out'][0][i][4] * input_data.shape[2])
                right = int(output['detection_out'][0][i][5] * input_data.shape[3])
                bottom = int(output['detection_out'][0][i][6] * input_data.shape[2])
                detections.append({
                    'class_id': class_id,
                    'confidence': confidence,
                    'bbox': (left, top, right, bottom)
                })
        return detections