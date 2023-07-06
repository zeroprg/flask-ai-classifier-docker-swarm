from PIL import Image
from yolo import process_image_yolov5
import db
import time
from io import BytesIO

currentime = int(round(time.time() * 1000))


def process_images(keys, images):   
    print (f"Images: {images[0]}")

    images[0].show()
    images[0].save('Tesing.jpg')

    currentime = int(round(time.time() * 1000))
    processed_results = process_image_yolov5(images)
    # Save the statistic of processed images to relative DB and return tuple of PILs to further processing :
    for i, result in enumerate(processed_results):
        print (f"result: {result}")
        key = keys[i]
        params = {}
        for item in enumerate(result[0]):
            _, label = item
            # Use the line before for testing
            #image.save(f'frame{i}_image{j}_of_{result[1][label]}{label}.jpg')
            # Save statistic info info table bellow
            #CREATE TABLE statistic ("type" text NULL,currentime int8 NULL,y int2 NULL,hashcodes VARCHAR(3000) NULL,cam uuid NULL)
            params['name'] = label
            params['x'] = currentime
            params['y'] = result[1][label]
            params['cam'] = key
            #params['hashcodes'] = ... use hash code algorithm in future if will be some logic to differenciate one image from another one by hashcodes
            try:
                db.insert_statistic(params)
            except Exception as e:
                print(f"Failed to insert statistic into database: {e}")

    return processed_results

