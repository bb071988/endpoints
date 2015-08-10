import os

from flask import Flask
from werkzeug.routing import Rule

app = Flask(__name__)
app.url_map.add(Rule('/api/', endpoint='index')) # added to allow delete method
config_path = os.environ.get("CONFIG_PATH", "posts.config.DevelopmentConfig")
app.config.from_object(config_path)

import api

from database import Base, engine
Base.metadata.create_all(engine)

