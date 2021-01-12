import os

from flask import Flask

#from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate

# Read all production configuration fro config.txt file
from project.config import ProductionConfig as prod
from project.db.api import Sql
import uuid
#from flask import g

""" 'Global' variables """
args = {}
imagesQueue = {}
detectors = {}
videos = []
vs = None

fps = None
p_get_frame = None
comp_uuid = str(uuid.uuid4())
db = Sql(SQLALCHEMY_DATABASE_URI = prod.SQLALCHEMY_DATABASE_URI)
def comp_node():
    return comp_uuid
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
