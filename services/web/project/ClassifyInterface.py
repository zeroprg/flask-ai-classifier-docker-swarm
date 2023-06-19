from abc import ABC, abstractmethod
class ClassifyInterface(ABC):
    @abstractmethod
    def classify(self, image):
        pass
    @abstractmethod
    def classify_and_save(self, image):
        pass