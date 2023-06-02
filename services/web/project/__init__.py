import os
import cv2
import CaffeClassifier
from flask import Flask


# Read all production configuration fro config.txt file
from project.config import ProductionConfig as prod
from project.db.api import Sql


def classify_init():
# Read configuration parameters    
    proto = prod.args['prototxt']
    model = prod.args['model']
    confidence_threshold = prod.args['confidence']
    if(model.find('caffe')>0): 
        cls = CaffeClassifier(proto, model, (64, 64, 64), confidence_threshold, if "DNN_TARGET_MYRIAD" in prod.args)
    else:
        net = cv2.dnn.readNet(proto, model)    
    # specify the target device as the Myriad processor on the NCS
    if "DNN_TARGET_MYRIAD" in prod.args:
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_MYRIAD)
    else:
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
    return net
    

db = Sql(SQLALCHEMY_DATABASE_URI = prod.SQLALCHEMY_DATABASE_URI)
net = classify_init()


def create_app(script_info=None):
    # instantiate the app    
    app = Flask(__name__)
    # Use this aproach when planning to use Models
    # set config (in flask-sqlAlchemy)    
    #app.config['SQLALCHEMY_DATABASE_URI'] = prod.SQLALCHEMY_DATABASE_URI
    # set up extensions
    #db.init_app(app)
    #migrate.init_app(app, db)

    # register blueprints
    from project.main import main_blueprint

    app.register_blueprint(main_blueprint)
    # shell context for flask cli   
    app.shell_context_processor({"app": app , "db": db})   
    
    return app