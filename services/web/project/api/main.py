import os
import logging
import json
import numpy as np
import cv2



from flask import Blueprint, jsonify, request
from project.api.classifyer import classify_frame
from project.config import  ProductionConfig as prod

SECRET_CODE = "secret" #open("/run/secrets/secret_code", "r").read().strip()

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
        "container_id": '????', #os.uname()[1],
    }
    #if request.get_json().get("secret") == SECRET_CODE:
    #    response_object["message"] = "yay!"
    return jsonify(response_object)

@main_blueprint.route('/classify', methods=['POST'])
def classify():
    data = request.json
    params = data['params']
    array = np.array(data['arr'])
    LOG.info("Hit /classify route: ", params, array.shape)
    post_array = classify_frame(net, array, params.cam )
    return json.dumps(post_array.tolist())
