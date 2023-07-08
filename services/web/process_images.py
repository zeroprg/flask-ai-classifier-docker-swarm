from PIL import Image
from project.yolo import process_image_yolov5
from project import db
import time


currentime = int(round(time.time() * 1000))


def process_images(keys, images):   
    print (f"Images: {len(images)}")
    currentime = int(round(time.time() * 1000))
    processed_results = process_image_yolov5(images)
    print (f"processed_results: {processed_results}")
    key = keys[0]
    for images, counts in processed_results:
        
        for image, label in images:
            # Unpack image and label
            print(image, label)
        params = {}
        # Unpack counts dictionary
        for label, count in counts.items():
            print(label, count)
            params['name'] = label
            params['x'] = currentime
            params['y'] = count
            params['cam'] = key
            print(f"label:{label} count: {count}")
            #params['hashcodes'] = ... use hash code algorithm in future if will be some logic to differenciate one image from another one by hashcodes
            try:
                db.insert_statistic(params)
            except Exception as e:
                print(f"Failed to insert statistic into database: {e}")
  
            

    return processed_results