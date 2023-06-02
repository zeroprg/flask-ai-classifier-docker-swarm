import os
import logging


from project.config_file import configure
# Read environment variables here : 

# set config
app_settings = os.getenv("APP_SETTINGS")
if app_settings is None or app_settings == '':
    app_settings = "./config.txt"


class ProductionConfig:
    """Production configuration"""

    LOGGING = os.environ.get("LOGGING") 
    PORT = os.environ.get("PORT")
    MAXIMUM_VIDEO_STREAMS =  os.environ.get("MAXIMUM_VIDEO_STREAMS")
    DB_USERNAME = os.environ.get("DB_USERNAME")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_PORT = os.environ.get("DB_PORT")
    DB_IP_ADDRESS = os.environ.get("DB_IP_ADDRESS")
    DB_NAME = os.environ.get("DB_NAME")
    CLASSIFIER_SERVER  = os.environ.get("CLASSIFIER_SERVER")

    CONFIDENCE=os.environ.get("CONFIDENCE")
    TRACK_MODIFICATIONS = False
    # read config file from app_settings
    args = configure(app_settings)
    if LOGGING is None:  LOGGING = logging.CRITICAL
    if DB_USERNAME is None or DB_USERNAME =='' : DB_USERNAME =  ( args["DB_USERNAME"] if ("DB_USERNAME" in args.keys()) else "postgres")
    if DB_PASSWORD is None or DB_PASSWORD =='' : DB_PASSWORD =  ( args["DB_PASSWORD"] if ("DB_PASSWORD" in args.keys()) else "postgres")
    if DB_PORT is None or DB_PORT =='' : DB_PORT =  (  args["DB_PORT"] if ("DB_PORT" in args.keys())  else "5432")
    if DB_NAME is None or DB_NAME =='' : DB_NAME =  (  args["DB_NAME"] if ("DB_NAME" in args.keys())  else "streamer")
    if DB_IP_ADDRESS is None or DB_IP_ADDRESS=='':
            DB_IP_ADDRESS =  args["DB_IP_ADDRESS"] if ("DB_IP_ADDRESS" in  args.keys()) else "192.168.0.100"
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format(DB_USERNAME, DB_PASSWORD, DB_IP_ADDRESS, DB_PORT, DB_NAME)
    if CLASSIFIER_SERVER is None or CLASSIFIER_SERVER =='' : CLASSIFIER_SERVER =  args["CLASSIFIER_SERVER"]
    if CONFIDENCE is None or CONFIDENCE =='' : CONFIDENCE =  args["confidence"]
    if MAXIMUM_VIDEO_STREAMS is None : MAXIMUM_VIDEO_STREAMS = args["MAXIMUM_VIDEO_STREAMS"] 
    MAXIMUM_VIDEO_STREAMS = int(MAXIMUM_VIDEO_STREAMS)
