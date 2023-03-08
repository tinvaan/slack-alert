
from flask import request, Blueprint

from .utils import signature
from .tasks.slack import Slack


alert = Blueprint('alert', __name__, url_prefix='/alert')


@alert.route('/bounced', methods=['POST'])
def notify():
    payload = request.get_json(force=True)
    bounce = payload.get('RecordType') == 'Bounce'
    spam = payload.get('TypeCode') == 512 and payload.get('Type') == 'SpamNotification'

    if bounce:
        if spam:
            Slack(payload).notify()
        return signature(data=payload, status=202 if spam else 200)

    return signature(status=400)
