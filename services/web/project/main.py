import os
import io
import zlib
import logging
import json
import numpy as np
import cv2
import base64
from PIL import Image


from flask import Blueprint, Response,request
import CaffeClassifier,ClassifyInterface

from flask_cors import cross_origin, CORS

from project import net

logging.basicConfig(level=logging.INFO)

SECRET_CODE = "secret" #open("/run/secrets/secret_code", "r").read().strip()
main_blueprint = Blueprint("main", __name__)
cors = CORS(main_blueprint, resources={r"/classify": {"origins": '*'}})

@main_blueprint.route("/ping", methods=["GET"])
def ping_pong():
    logging.info('Hitting the "/ping" route')
    return Response(json.dumps({"status": "success", "message": "ping-pong!", "container_id": os.uname()[1]},
                               default=str, indent = 4), mimetype='text/plain', status=200)



@main_blueprint.route("/secret", methods=["GET"])
def secret():
    logging.info('Hitting the "/secret" route')
    response_object = {
        "status": "success",
        "message": "nay!",
        "container_id": os.uname()[1],
    }

    return Response(json.dumps(response_object,
                               default=str, indent = 4), mimetype='text/plain', status=200)


# Take in base64 string and return PIL image
def stringToImage(base64_string):
    imgdata = base64.b64decode(base64_string)
    return Image.open(io.BytesIO(imgdata))

def from_base64(base64_data):
    nparr = np.fromstring(base64.b64decode(base64_data), np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)

@main_blueprint.route('/classify', methods=['POST'])
@cross_origin(origin='*')
def classify():
    data = request.get_json()
    params = data['parameters']
    im_b64 = data['image']
    logging.info("cam: {0} , confidence: {1} data: {2}".format(params['cam'], params['confidence'], im_b64))
    # get the base64 encoded string
    # convert it into bytes  
    #img_bytes = base64.b64decode(im_b64.encode('utf8'))
    
    # convert bytes data to PIL Image object
    #img = Image.open(io.BytesIO(img_bytes))
    img = from_base64(im_b64)
  
    
    #base64_data = str(data['array'])    
    #if (base64_data is None ): return jsonify({"status": "failed", "message": "image frame is NoneType"})
    #decodedArrays = json.loads(str(data['array']))
    #logging.info("decodedArrays: " + decodedArrays)
    #frame = Image.fromarray(np.asarray(decodedArrays))    
    #frame =  from_base64(base64_data)
    logging.debug("Hit /classify route: ", params)
    classifyI = ClassifyInterface()
    post_array = classifyI.classify_frame(net, img, params)
    return Response(json.dumps(post_array, default=str, indent = 4),  mimetype='text/plain', status=200)


def uncompress_nparr(bytestring):
    """ Uncompressed the bytestring values """
    return np.load(io.BytesIO(zlib.decompress(bytestring)))
