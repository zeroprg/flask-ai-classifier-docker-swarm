import uuid
import logging
import requests
import socket
import cv2
from urllib.parse import urlsplit

#from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate

# Read all production configuration fro config.txt file
from project.config import ProductionConfig as prod
from project.db.api import Sql
from flask import Response

#from flask import g

logging.basicConfig(level=logging.INFO)

""" 'Global' variables """
DELETE_FILES_LATER = 72 #   ( 3 days in hours)
URL_PINGS_NUMBER = 1 # delete process which use this URL after that pings
delete_expired_streams_interval = 200 #secs
update_urls_from_stream_interval = 100 #secs
clean_up_service_interval = 3600*24 #secs


args = {}
#imagesQueue = {}
detectors = {}
videos = []
vs = None

fps = None
p_get_frame = None

comp_uuid = str(uuid.uuid4())
def comp_node():
    return comp_uuid

def url_to_filename(url):
    """Convert a URL to a valid filename by removing special characters."""
    return "".join(c for c in url if c.isalnum() or c in (".", "_")) + ".txt"

def geSession():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }
    
    session = requests.Session()
    session.headers.update(headers)
    return session;

# Store information to a file
def store_info(filename, last_visit_url, visited_urls):
    with open(filename, "w") as file:
        file.write("last_visit_url=" + last_visit_url + "\n")
        for url in visited_urls:
            file.write(url + "\n")

# Read information from a file
def read_info(filename):
    last_visit_url = None
    visited_urls = set()
    try:
        with open(filename, "r") as file:
            for line in file:
                if line.startswith("last_visit_url="):
                    last_visit_url = line[len("last_visit_url="):].strip()
                else:
                    visited_urls.add(line.strip())
    except FileNotFoundError:
        logging.info("file name {} was not founded".format(filename))          
    return last_visit_url, visited_urls

def ping_video_url(url):
    """ Ping url """
    try:
        vs = cv2.VideoCapture(url)
        flag, _ = vs.read()
    except Exception as e:        
        logging.critical("Exception in ping url: {}".format(e))   
        
    return flag

db = Sql(SQLALCHEMY_DATABASE_URI = prod.SQLALCHEMY_DATABASE_URI)


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
  

def populate_urls_in_db(add_url):
    logging.info('adding a new video urls ' + add_url)
    if ping_video_url(add_url):
        try:
            params = { 'url': add_url }
            populate_lat_long(params)
            db.insert_urls(params)
        except Exception as e:
            logging.critical("Exception during saving url:{} : {}".format(add_url,e))
            msg = "URL already exist it was already  added successfully"
            return Response({"message":msg}, mimetype='text/plain', status=500)           
        else:     
            logging.info("URL {} added successfully".format(add_url))           
            return Response('{"message":"URL added successfully"}', mimetype='text/plain',status=200)
    else:
        logging.info("URL {} has no video".format(add_url))
        return Response('{"message":"URL has no video"}', mimetype='text/plain',status=400)

