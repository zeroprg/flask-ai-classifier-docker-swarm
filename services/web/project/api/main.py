import os
import io
import zlib
import logging
import json
import numpy as np
import cv2
import base64
from PIL import Image


from flask import Blueprint, Response, jsonify, request, g
from project.api.classifyer import classify_frame
from project.config import  ProductionConfig as prod
import project.api.tools.config_file

from project import db

SECRET_CODE = "secret" #open("/run/secrets/secret_code", "r").read().strip()
LOG = logging.getLogger("classifier-api.error")

main_blueprint = Blueprint("main", __name__)

def get_net():
    if 'net' not in g:
        g.net = classify_init()
    return g.net

def classify_init():
# Read configuration parameters
    net = None
    classifyer = 'CaffeModel'
    if classifyer == 'CaffeModel':
        proto = prod.args['prototxt']
        model = prod.args['model']
        net = cv2.dnn.readNetFromCaffe(proto, model)
    elif classifyer == 'YOLO':
            proto = prod.args['prototxt']
            model = prod.args['model']
            net = cv2.dnn.readNetFromCaffe(proto, model)
    # specify the target device as the Myriad processor on the NCS
    if "DNN_TARGET_MYRIAD" in prod.args:
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_MYRIAD)
    else:
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
    return net
    



@main_blueprint.route("/ping", methods=["GET"])
def ping_pong():
    LOG.info('Hitting the "/ping" route')
    return jsonify(
        {"status": "success", "message": "ping-pong!", "container_id": os.uname()[1]}
    )


@main_blueprint.route("/secret", methods=["GET"])
def secret():
    LOG.info('Hitting the "/secret" route')
    response_object = {
        "status": "success",
        "message": "nay!",
        "container_id": os.uname()[1],
    }
    #if request.get_json().get("secret") == SECRET_CODE:
    #    response_object["message"] = "yay!"
    return jsonify(response_object)


# Take in base64 string and return PIL image
def stringToImage(base64_string):
    imgdata = base64.b64decode(base64_string)
    return Image.open(io.BytesIO(imgdata))

def from_base64(base64_data):
    nparr = np.fromstring(base64.b64decode(base64_data), np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)

@main_blueprint.route('/classify', methods=['POST'])
def classify():
    net = get_net()
    data = request.get_json()
    params = data['params']
    print("cam: {0} , confidence: {1} ".format(params['cam'], params['confidence']))
    base64_data = str(data['array'])
    if (base64_data is None ):
	    return jsonify(
        	{"status": "failed", "message": "np array is NoneType"}
	    )
    frame =  from_base64(base64_data)
    LOG.info("Hit /classify route: ", params)
    post_array = classify_frame(net, frame, params['cam'], params['confidence'])
    return Response(json.dumps(post_array), mimetype='text/plain')

def uncompress_nparr(bytestring):
    """ Uncompressed the bytestring values """
    return np.load(io.BytesIO(zlib.decompress(bytestring)))
