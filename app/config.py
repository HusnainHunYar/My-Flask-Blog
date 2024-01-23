import json
from app import app
from flask_mail import Mail
with open('config.json', 'r') as c:
    parameters = json.load(c)["parameters"]


class Config:
    UPLOAD_FOLDER = parameters['upload_location']
    SECRET_KEY = 'super-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = parameters['local_uri']  # Change this to your database URI
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = '465'
    MAIL_USE_SSL = True
    MAIL_USERNAME = parameters['gmail_username']
    MAIL_PASSWORD = parameters['gmail_password']
    mail = Mail(app)
