import os
import logging


from project.config_file import configure
# Read environment variables here : 

# set config
app_settings = os.getenv("APP_SETTINGS")
if app_settings is None or app_settings =='' :app_settings = "./config.txt"


class ProductionConfig:
    """Production configuration"""
    DB_USERNAME = os.environ.get("DB_USERNAME")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_PORT = os.environ.get("DB_PORT")
    DB_IP_ADDRESS = os.environ.get("DB_IP_ADDRESS")
    DB_NAME = os.environ.get("DB_NAME")
    CLASSIFIER_SERVER  = os.environ.get("CLASSIFIER_SERVER")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    TRACK_MODIFICATIONS = False
    # read config file from app_settings
    args = configure(app_settings)
    if DB_USERNAME is None or DB_USERNAME =='' : DB_USERNAME =  ( args["DB_USERNAME"] if ("DB_USERNAME" in args.keys()) else "postgres")
    if DB_PASSWORD is None or DB_PASSWORD =='' : DB_PASSWORD =  ( args["DB_PASSWORD"] if ("DB_PASSWORD" in args.keys()) else "postgres")
    if DB_PORT is None or DB_PORT =='' : DB_PORT =  (  args["DB_PORT"] if ("DB_PORT" in args.keys())  else "5432")
    if DB_NAME is None or DB_NAME =='' : DB_NAME =  (  args["DB_NAME"] if ("DB_NAME" in args.keys())  else "streamer")
    if SQLALCHEMY_DATABASE_URI is None or SQLALCHEMY_DATABASE_URI=='':
        if DB_IP_ADDRESS is not None or args["DB_IP_ADDRESS"] is not None:
            DB_IP_ADDRESS =  args["DB_IP_ADDRESS"] if ("DB_IP_ADDRESS" in  args.keys()) else "192.168.0.167"
            SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format(DB_USERNAME, DB_PASSWORD, DB_IP_ADDRESS, DB_PORT, DB_NAME)
        else:
            SQLALCHEMY_DATABASE_URI = 'sqlite://frame.db'

    if CLASSIFIER_SERVER is None or CLASSIFIER_SERVER =='' : CLASSIFIER_SERVER =  args["CLASSIFIER_SERVER"]


