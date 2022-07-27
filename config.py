import os
from dotenv import load_dotenv
import cloudinary
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))
# gives access to the project in any OS we find ourselves in
# Allows outside files/folders to be added to the project from the base directory


class Config():
    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_ENV = os.environ.get('FLASK_ENV')
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'SOMETHING'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEPLOY_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    CLOUD_NAME = os.getenv('CLOUD_NAME')
    API_KEY=os.getenv('API_KEY')
    API_SECRET=os.getenv('API_SECRET')
    # turns off updates messages from sqlalchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False

cloudinary.config(cloud_name = os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), api_secret=os.getenv('API_SECRET'))

