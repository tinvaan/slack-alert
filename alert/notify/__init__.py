
from flask import Flask

from .tasks import taskify


app = Flask('notify', instance_relative_config=True)
app.config.from_object('alert.config')
app.config.from_pyfile('config.py', silent=True)


# Setup task queue
queue = taskify(app)


# Register app blueprints
from .views import alert

app.register_blueprint(alert)
