import abc

class NeuralNetwork(abc.ABC):
    @abc.abstractmethod
    def __init__(self, model_path, weights_path):
        pass

    @abc.abstractmethod
    def predict(self, input_data, detection_classes=None, confidence_thresh=0.5, nms_thresh=0.45):
        pass
