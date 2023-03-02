
from flask import Flask, request

from .tasks import slack


app = Flask('notify', instance_relative_config=True)
app.config.from_object('alert.config')
app.config.from_pyfile('config.py', silent=True)


@app.route('/alert/notify/slack', methods=['POST'])
def notify():
    payload = request.get_json(force=True)
    if (payload.get('TypeCode') == 512 and
        payload.get('Type') == 'SpamNotification'
    ):
        return slack.send(payload)

    return {'error': 'Bad Request'}, 400
