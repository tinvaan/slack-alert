
from flask import jsonify, make_response


def signature(data=None, status=200):
    if status == 400:
        return make_response(jsonify({'error': 'Bad Request'}), 400)

    return make_response(jsonify({
        'Type': data.get('Type'),
        'Email': data.get('Email'),
        'BouncedAt': data.get('BouncedAt'),
        'Description': data.get('Description'),
        'Tag': data.get('Tag')
    }), status)
