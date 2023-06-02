import cv2
import os
import torch
import numpy as np
from PIL import Image
import base64
from io import BytesIO

class YoloClassifier():
    def __init__(self, confidence_threshold):
        self.confidence_threshold = confidence_threshold

        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
        self.classes = ['person', 'cat', 'dog']

    def classify(self, img):
        results = self.model([img], size=640) # Perform inference on a single image

        # Get the predictions
        predictions = results.xyxy[0]

        # Filter predictions for specified classes
        predictions = predictions.cpu().numpy()
        class_id = predictions[:, 5].astype(int)  # Convert class_id to integers
        filtered_predictions = predictions#[np.isin(class_id, self.classes)]

        #print("Filtered Predictions Shape:", filtered_predictions.shape)
        #print("Filtered Predictions Content:", filtered_predictions)

        # Print the class names and confidence scores
        for box in filtered_predictions:
            x1, y1, x2, y2, _, class_id = box
            print(self.model.names[int(class_id)])
            #print(confidence)

        # Save the filtered predicted images
        images = []
        for box in filtered_predictions:
            
            x1, y1, x2, y2, _, class_id = box

            if self.model.names[int(class_id)] in self.classes:
                cropped_image = img.crop((x1, y1, x2, y2))
                images.append(cropped_image)

        return images

    def save(self, img, output_path=None):
        if output_path:
            output_dir = os.path.dirname(output_path)
            os.makedirs(output_dir, exist_ok=True)  # Create the output directory if it doesn't exist
            img.save(output_path)
        else:
            # Convert the image to base64 encoded text
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            img_b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            # Store the base64 encoded image in the database
            # Replace 'db_store_image()' with your actual method to store the image in the database
           # db_store_image(img_b64)

    def classify_and_save(self, img, output_dir):
        filtered_images = self.classify(img)
        for i, img in enumerate(filtered_images):
            file_path = f"{output_dir}/filtered_image_{i}.png"
            self.save(img, file_path)


if __name__ == "__main__":
    image_path = './tests/woman.jpg'
    pil_image = Image.open(image_path).convert("RGB")
    
    classifier = YoloClassifier(0.5) 
    classifier.classify_and_save(pil_image, output_dir='./output')
