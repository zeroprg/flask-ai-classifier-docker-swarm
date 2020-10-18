import os
import logging


from project.api.tools.config_file import configure

USER = os.environ.get("DB_USER")
PASSWORD = os.environ.get("DB_PASSWORD")
if USER is None or USER =='' : USER = "postgres"
if PASSWORD is None or PASSWORD =='' : PASSWORD =  "postgres"
# set config
app_settings = os.getenv("APP_SETTINGS")
if app_settings is None or app_settings =='' :app_settings = "config.txt"


class ProductionConfig:
    """Production configuration"""

    TRACK_MODIFICATIONS = False
    DATABASE_URI = f"postgres://{USER}:{PASSWORD}@db:5432/streamer"
    # read config file from app_settings
    args = configure(app_settings)
