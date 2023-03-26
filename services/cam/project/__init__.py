from flask import Flask
import uuid
import logging
import requests
import socket
import cv2
import imutils
import re
from urllib.parse import urlsplit

#from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate

# Read all production configuration fro config.txt file
from project.config import ProductionConfig as prod
from project.db.api import Sql


#from flask import g


''' Rules specify topic of the frame based by founded objects '''

topic_rules = {
    "people": (["person"], 1),
    "traffic": (["car", "bus", "road","traffic light"],2),
    "office":  (["tvmonitor","chair", "sofa", "table"],2),   
    "vehicles": (["car", "bus", "train", "motorbike", "bicycle"], 2),
    "bedroom":  (["person", "sofa", "bed"],  2),
    "furniture": (["chair", "sofa", "bed", "table", "diningtable"], 2),
    "animals": (["cat", "dog", "horse", "cow", "sheep", "bird", "fish", "turtle"], 1),
    "kitchen": (["oven", "microwave", "refrigerator", "sink", "blender"], 2),
    "outdoor": (["tree", "flower", "building", "sky", "grass"], 3), 
    "water": (["boat", "swimming pool", "beach", "surfboard", "umbrella"], 2),
    "tools_and_electronics": (["hammer", "screwdriver", "wrench", "scissors", "knife", "tvmonitor", "laptop", "cellphone", "mouse", "keyboard"], 2),
    "indoor_and_furniture": (["lamp", "book", "clock", "vase", "painting", "chair", "sofa", "bed", "table", "diningtable"], 2),
    "outdoor_and_nature": (["tree", "flower", "grass", "mountain", "waterfall"], 1),
    "vehicles_and_traffic": (["car", "bus", "train", "motorbike", "bicycle", "traffic light", "stop sign"], 2),
    "construction": (["crane", "tractor", "construction vehicle", "hard hat", "safety vest"], 2),
    "electronics": (["tvmonitor", "laptop", "cellphone", "mouse", "keyboard"], 2),  
    "tools": (["hammer", "screwdriver", "wrench", "scissors", "knife"], 2),    
    "sports": (["ball", "tennis racket", "baseball glove", "ski", "skateboard"], 2),
    "music": (["guitar", "piano", "drums", "microphone", "violin"], 2),
    "medical": (["stethoscope", "syringe", "medicine", "doctor", "nurse"], 2),
    "technology": (["robot", "drone", "computer", "server", "chip"], 2),
    "science": (["test tube", "microscope", "telescope", "atom", "planet"], 1),    
}


""" 'Global' variables """
DELETE_FILES_LATER = 72 #   ( 3 days in hours)
URL_PINGS_NUMBER = 1 # deny process from serice after that pings in update_urls_from_stream_interval
delete_expired_streams_interval = 600 #secs
update_urls_from_stream_interval = 120 #secs
clean_up_service_interval = 3600*24 #secs
NUMBER_OF_THREADS = 1 # thread per Detector  

args = {}
#imagesQueue = {}
detectors = {}
videos = []
vs = None

fps = None
p_get_frame = None

comp_uuid = None
def comp_node():
    global comp_uuid
    if(comp_uuid is None ): comp_uuid = str(uuid.uuid4())
    return comp_uuid

db = Sql(SQLALCHEMY_DATABASE_URI = prod.SQLALCHEMY_DATABASE_URI)

# instantiate the extensions
#migrate = Migrate()

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


def populate_lat_long(params):
    if( 'lat' in params ): return  
    data = get_geolocation_by_ip(convert_url_to_ip(params['url']))
    if(data is not None and 'location' in data ):
        params['lat'] = data['location']['lat']
        params['lng'] = data['location']['lng']
        params['city'] =  data['location']['city']
        params['postalcode'] =  data['location']['postalCode']
        params['country'] =  data['location']['country']
    

ip_geolocation_key = None
def get_geolocation_by_ip(ip): 
    global ip_geolocation_key
    if( ip_geolocation_key is None):
        with open('api_key.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                if 'ip_geolocation' in line.lower():
                    ip_geolocation_key = line.strip().split('=')[1]
                    break

    headers = {
        "X-RapidAPI-Key": ip_geolocation_key,
        "X-RapidAPI-Host": "whoisapi-ip-geolocation-v1.p.rapidapi.com"
    }
    json_response = None
    url = "https://whoisapi-ip-geolocation-v1.p.rapidapi.com/api/v1?ipAddress={}".format(ip)
    try:
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()
        json_response = response.json()
        logging.debug("Entire JSON response: {}".format(json_response))
    except requests.exceptions.HTTPError as http_err:
        logging.critical("HTTP error occurred: {}".format(http_err) )
    except Exception as err:
        logging.critical("Failed to get geolocation by IP: {}".format(err))
    return json_response

def get_hostname(url):
    result = urlsplit(url)
    return result.hostname

def convert_url_to_ip(url):
    try:        
        hostname = get_hostname(url)
        logging.debug("convert_url_to_ip: {}".format(hostname))
        if(hostname is None): return None
        return socket.gethostbyname(hostname)
    except socket.gaierror as e:
        logging.critical("Error resolving hostname: {}".format(e))
        return None
    
google_api_key = None
def search_with_google(query):
    global google_api_key
    if( google_api_key is None):
        with open('api_key.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                if 'google_search' in line.lower():
                    google_api_key = line.strip().split('=')[1]
                    break

    url = "https://www.googleapis.com/customsearch/v1?q={}&key={}".format(query, google_api_key)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        items = data.get("items", [])
        urls = [item.get("link", "") for item in items]
        return urls
    else:
        return []
    
image_check = r'(?<!/cgi-bin/).*\.(?!mjpg)(?!mjpeg)(jpg|jpeg|png|gif|bmp)\b|\b[jJ][pP][eE]?[gG]\b|shot|/image/'
simple_decode = r'.*\.(cgi|mjpg|mjpeg)$|\b/cgi-bin/|\baction=stream'
def ping_video_url(url):
    """ Ping url """
    flag = False
    try:
        if "/cgi-bin/" not in url and  bool(re.search(r'.*\.(?!mjpg)(jpg|jpeg|png|gif|bmp)\b|\b[jJ][pP][eE]?[gG]\b|shot|/image/', url, re.IGNORECASE)):
            imutils.url_to_image(url)
            flag = True
        else:                
            vs = cv2.VideoCapture(url)
            flag, _ = vs.read()
    except Exception as e:        
        logging.debug("Exception in ping url: {}".format(e))        
    return flag
