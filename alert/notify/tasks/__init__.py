
from celery import Celery


def taskify(app):
    with app.app_context():
        q = Celery(app.name, broker=app.config.get('CELERY_BROKER_URL'))
        q.conf.update(app.config)
        return q
