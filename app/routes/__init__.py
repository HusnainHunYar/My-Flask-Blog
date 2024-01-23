from flask import Flask
from app.models import db
import os

app = Flask(__name__)
app.config.from_object('app.config.Config')
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.template_folder = os.path.abspath('templates')
app.static_folder = os.path.abspath('static')
db.init_app(app)

from app.routes import auth, blog

app.register_blueprint(auth.bp)
app.register_blueprint(blog.bp)
