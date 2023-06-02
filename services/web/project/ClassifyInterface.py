from abc import ABC, abstractmethod
class ClassifyInterface(ABC):
    @abstractmethod
    def classify(self, image):
        pass