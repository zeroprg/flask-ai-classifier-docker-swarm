import os
import io
import zlib
import logging
import json
import numpy as np
import cv2



from flask import Blueprint, jsonify, request
from project.api.classifyer import classify_frame
from project.config import  ProductionConfig as prod
import project.api.tools.config_file
SECRET_CODE = "secret" #open("/run/secrets/secret_code", "r").read().strip()
LOG = logging.getLogger("classifier-api.error")

main_blueprint = Blueprint("main", __name__)
net = None

@main_blueprint.route("/init", methods=["POST"])
def classify_init():
# Read configuration parameters
    classifyer = request.get_json().get("classifyer")
    if classifyer == 'CaffeModel':
        proto = prod.args['prototxt-caffe']
        model = prod.args['model-caffe']
        net = cv2.dnn.readNetFromCaffe(proto, model)
        response_object["message"] = "Successefuly changed to Caffe!"
    elif classifyer == 'YOLO':
            proto = prod.args['prototxt-yolo']
            model = prod.args['model-yolo']
            net = cv2.dnn.readNetFromCaffe(proto, model)
            response_object["message"] = "Successefuly changed to YOLO!"

    # specify the target device as the Myriad processor on the NCS
    if "DNN_TARGET_MYRIAD" in prod.args:
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_MYRIAD)
    else:
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)


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
    data = request.json
    params = data['params']
    bytestring = data['array']
    frame = uncompress_nparr(bytestring)
    LOG.info("Hit /classify route: ", params)
    post_array = classify_frame(net, frame, params.cam, params.confidence)
    return json.dumps(post_array.tolist())

def uncompress_nparr(bytestring):
    """ Uncompressed the bytestring values """
    return np.load(io.BytesIO(zlib.decompress(bytestring)))