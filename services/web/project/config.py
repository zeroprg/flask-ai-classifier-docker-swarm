import os



from project.tools.config_file import configure

USER = os.environ.get("DB_USER")
PASSWORD = os.environ.get("DB_PASSWORD")
if USER is None or USER =='' : USER = "postgres"
if PASSWORD is None or PASSWORD =='' : PASSWORD =  "postgres"
# set config
app_settings = os.getenv("APP_SETTINGS")
if app_settings is None or app_settings =='' :app_settings = "./config.txt"


class ProductionConfig:
    """Production configuration"""
    DB_USERNAME = os.environ.get("DB_USERNAME")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_PORT = os.environ.get("DB_PORT")
    DB_NAME = os.environ.get("DB_NAME")

    KAFKA_SERVER  = os.environ.get("KAFKA_SERVER")
    #ZOOKEEPERS = os.environ.get("ZOOKEEPERS")
    KAFKA_PREPROCESSED_TOPIC  = os.environ.get("KAFKA_PREPROCESSED_TOPIC")
    #KAFKA_POSTPROCESSED_TOPIC  = os.environ.get("KAFKA_POSTPROCESSED_TOPIC")

    CLASSIFIER_SERVER  = os.environ.get("CLASSIFIER_SERVER")
    DB_IP_ADDRESS = os.environ.get("DB_IP_ADDRESS")
    TRACK_MODIFICATIONS = False
    # read config file from app_settings
    args = configure(app_settings)
    if DB_USERNAME is None or DB_USERNAME =='' : DB_USERNAME =  ( args["DB_USERNAME"] if ("DB_USERNAME" in args.keys()) else "postgres")
    if DB_PASSWORD is None or DB_PASSWORD =='' : DB_PASSWORD =  ( args["DB_PASSWORD"] if ("DB_PASSWORD" in args.keys()) else "postgres")
    if DB_PORT is None or DB_PORT =='' : DB_PORT =  (  args["DB_PORT"] if ("DB_PORT" in args.keys())  else "5432")
    if DB_NAME is None or DB_NAME =='' : DB_NAME =  (  args["DB_NAME"] if ("DB_NAME" in args.keys())  else "streamer")
    if DB_IP_ADDRESS is None or DB_IP_ADDRESS=='': 
            DB_IP_ADDRESS =  args["DB_IP_ADDRESS"] if ("DB_IP_ADDRESS" in  args.keys()) else "192.168.0.100"
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format(DB_USERNAME, DB_PASSWORD, DB_IP_ADDRESS, DB_PORT, DB_NAME)        
    if KAFKA_SERVER is None or KAFKA_SERVER =='' : KAFKA_SERVER =  args["KAFKA_SERVER"]
    if CLASSIFIER_SERVER is None or CLASSIFIER_SERVER =='' : CLASSIFIER_SERVER =  args["CLASSIFIER_SERVER"]
    if KAFKA_PREPROCESSED_TOPIC is None or KAFKA_PREPROCESSED_TOPIC =='' : KAFKA_PREPROCESSED_TOPIC =  args["KAFKA_PREPROCESSED_TOPIC"]
    #if KAFKA_POSTPROCESSED_TOPIC is None or KAFKA_POSTPROCESSED_TOPIC =='' : KAFKA_POSTPROCESSED_TOPIC =  args["KAFKA_POSTPROCESSED_TOPIC"]
    #if ZOOKEEPERS is None or ZOOKEEPERS =='' : ZOOKEEPERS =  args["ZOOKEEPERS"]