import os
import io
import zlib
import logging
import json
import numpy as np
import cv2




from flask import Blueprint, Response, jsonify, request
from project.api.classifyer import classify_frame
from project.config import  ProductionConfig as prod
import project.api.tools.config_file
SECRET_CODE = "secret" #open("/run/secrets/secret_code", "r").read().strip()
LOG = logging.getLogger("classifier-api.error")

main_blueprint = Blueprint("main", __name__)


from flask import g

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
        response_object["message"] = "Successefuly changed to Caffe!"
    elif classifyer == 'YOLO':
            proto = prod.args['prototxt']
            model = prod.args['model']
            net = cv2.dnn.readNetFromCaffe(proto, model)
            response_object["message"] = "Successefuly changed to YOLO!"

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
        {"status": "success", "message": "pong!", "container_id": os.uname()[1]}
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

@main_blueprint.route('/classify', methods=['POST'])
def classify():
    net = get_net()
    data = request.get_json()
    params = data['params']
    print("cam: {0} , confidence: {1} ".format(params['cam'], params['confidence']))
    bytestring = data['array']
    if (bytestring is None ):
	    return jsonify(
        	{"status": "failed", "message": "np array is NoneType"}
	    )
    #print(bytestring)
    #frame =  np.array(bytestring) # uncompress_nparr(bytestring)
       # convert string of image data to uint8
    frame = np.fromstring(bytestring, np.uint8)
    print(frame)
    LOG.info("Hit /classify route: ", params)
    post_array = classify_frame(net, frame, params['cam'], params['confidence'])
    return Response(json.dumps(post_array), mimetype='text/plain')

def uncompress_nparr(bytestring):
    """ Uncompressed the bytestring values """
    return np.load(io.BytesIO(zlib.decompress(bytestring)))
