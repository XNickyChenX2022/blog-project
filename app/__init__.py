import os
from flask import Flask
from flask_session import Session
from .config import Config
from .extensions import db
from sqlalchemy import DDL

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'your_secret_key'
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
db.init_app(app)

from app import views
from app import models
from app import auth