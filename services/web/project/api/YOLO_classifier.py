import cv2
import numpy as np
import time

def classify_frame(frame, params, net=None):
    if net is None:
        # Load the YOLOv4 model
        net = cv2.dnn.readNetFromDarknet("yolov4.cfg", "yolov4.weights")
    
    # Set the input to the model as the frame
    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
                                 swapRB=True, crop=False)
    net.setInput(blob)
    
    # Get the predictions from the model
    layers_names = net.getLayerNames()
    output_layers = [layers_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    outputs = net.forward(output_layers)
 
    
    # Initialize a list to store the detected objects
    objects = []
    
    # Loop through the predictions
    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            
            # Only consider detections with a confidence above the given threshold
            if confidence > params['confidence']:
                # Get the bounding box for the detected object
                center_x = int(detection[0] * frame.shape[1])
                center_y = int(detection[1] * frame.shape[0])
                w = int(detection[2] * frame.shape[1])
                h = int(detection[3] * frame.shape[0])
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                
                # Store the object information in a list
                objects.append({'class_id': class_id, 'confidence': confidence, 'x': x, 'y': y, 'w': w, 'h': h})
    
    # Return the list of objects
    return {'objects': objects}
