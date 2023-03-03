
from flask import Flask, request, jsonify, make_response

from .tasks import slack


app = Flask('notify', instance_relative_config=True)
app.config.from_object('alert.config')
app.config.from_pyfile('config.py', silent=True)


@app.route('/alert/bounced', methods=['POST'])
def notify():
    payload = request.get_json(force=True)
    if payload.get('RecordType') == 'Bounce':
        if payload.get('TypeCode') == 512 and payload.get('Type') == 'SpamNotification':
            return make_response(slack.send(payload), 202)

        return jsonify({
            'Type': payload.get('Type'),
            'Email': payload.get('Email'),
            'BouncedAt': payload.get('BouncedAt'),
            'Description': payload.get('Description'),
            'Tag': payload.get('Tag')
        })

    return {'error': 'Bad Request'}, 400
