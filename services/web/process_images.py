from PIL import Image
import time

from project.yolo import process_image_yolov5
from project import db

def generate_hashcode(image):
    # Convert the array to a string
    bytes = image.tobytes()
    # Generate the hash code using the string representation
    hashcode = hash(bytes)
    return hashcode

def process_images(keys, images):   
    print(f"Images: {len(images)}")
    current_time = int(round(time.time() * 1000))
    processed_results = process_image_yolov5(images)
    print(f"processed_results: {processed_results}")
   
    
    for i,result in enumerate(processed_results):
        key = keys[i]
        images, counts = result
        hashes = []
        for image, label in images:
            # Unpack image and label
            hash_code = generate_hashcode(image)
            print(image, label, hash_code)
            hashes.append(hash_code)

        hashes_str = "['" + "', '".join(str(i) for i in  hashes) + "']"
        for label, count in counts.items():
            print(label, count)
            
            params = {
                'name': label,
                'x': current_time,
                'y': count,
                'cam': key,
                'hashcodes': hashes_str
            }
            
            print(f"label: {label}, count: {count}")
            
            try:
                db.insert_statistic(params)
            except Exception as e:
                print(f"Failed to insert statistic into database: {e}")           

    return processed_results
