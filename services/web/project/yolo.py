import torch
from PIL import Image
import pandas as pd


# Tuple of labels to filter
label_tuple = ('person', 'dog', 'cow')

# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s') 

    
# Set the device and torch data type
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"CUDA is available :{torch.cuda.is_available()} .")


class_labels = model.names

def process_image_yolov5(images):


    # Inference
    results = model(images, size=320)

    # Processed results
    processed_results = []

    # Process the images
    for image, result in zip(images, results.xyxy):
        result_array = result.cpu().numpy()
        result_df = pd.DataFrame(result_array, columns=['xmin', 'ymin', 'xmax', 'ymax', 'confidence', 'class'])
        filtered_images = get_processed_images(image, result_df)
        processed_results.append(filtered_images)

    return processed_results


def get_processed_images(image, result):
    processed_images = []
    # Collect object counts by label
    object_counts = {}
    for _, row in result.iterrows():
        label_index = int(row['class'])
        label = class_labels[label_index]
        print(f"label = {label}")
        
        # Update object count
        if label in object_counts:
            object_counts[label] += 1
        else:
            object_counts[label] = 1

        if label in label_tuple:
            x1, y1, x2, y2 = row[['xmin', 'ymin', 'xmax', 'ymax']].astype(int)            
            cropped_image = image.crop((x1, y1, x2, y2))
            processed_images.append((cropped_image, label))

    #result: (((<PIL.Image.Image image mode=RGB size=175x494 at 0x7F00099F4850>, 0.0),
               #(<PIL.Image.Image image mode=RGB size=131x463 at 0x7F00012A1610>, 0.0), 
               #(<PIL.Image.Image image mode=RGB size=139x469 at 0x7F00012A1490>, 0.0)), 
               #{'person': 3, 'bus': 1})
    return tuple(processed_images),object_counts 


# Example usage

if __name__ == "__main__":
    images = [
        Image.open('./tests/zidane.jpg'),
        Image.open('./tests/bus.jpg')
    ]


    processed_results = process_image_yolov5(images)

    # Save the processed images
    for i, result in enumerate(processed_results):
        print (f"result: {result}")
        for j, item in enumerate(result[0]):
            image, label = item
            image.save(f'frame{i}_image{j}_of_{result[1][label]}{label}.jpg')
