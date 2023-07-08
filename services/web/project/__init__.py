
# Read all production configuration fro config.txt file
from project.config import ProductionConfig as prod
from project.db.api import Sql

db = Sql(SQLALCHEMY_DATABASE_URI = prod.SQLALCHEMY_DATABASE_URI)
