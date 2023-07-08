from PIL import Image
from project.yolo import process_image_yolov5
from project import db
import time

def process_images(keys, images):   
    print(f"Images: {len(images)}")
    current_time = int(round(time.time() * 1000))
    processed_results = process_image_yolov5(images)
    print(f"processed_results: {processed_results}")
   
    
    for i,result in enumerate(processed_results):
        key = keys[i]
        images, counts = result

        for image, label in images:
            # Unpack image and label
            print(image, label)
        
        for label, count in counts.items():
            print(label, count)
            
            params = {
                'name': label,
                'x': current_time,
                'y': count,
                'cam': key
            }
            
            print(f"label: {label}, count: {count}")
            
            try:
                db.insert_statistic(params)
            except Exception as e:
                print(f"Failed to insert statistic into database: {e}")           

    return processed_results
