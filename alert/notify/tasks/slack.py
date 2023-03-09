
import json
import logging

from flask import current_app as app
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from .. import queue


def initialize():
    if not app.config.get('slack', {}).get('client'):
        app.config.slack = {
            'client': WebClient(token=app.config.get('SLACK_CHANNEL_BOT_TOKEN'))
        }
    return app.config.slack.get('client')


def content(data):
    return json.dumps([
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": data.get('Name')
            }
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*Email:* %s" % data.get('Email')
                }
            ]
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*When:* %s" % data.get('BouncedAt')
                }
            ]
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Description:* %s" % data.get('Description')
            }
        }
    ])

@queue.task
def notify(data):
    client = initialize()

    try:
        response = client.chat_postMessage(channel=app.config.get('SLACK_CHANNEL_NAME'),
                                           text=content(data), blocks=content(data))
    except SlackApiError as e:
        logging.error('Failed to post alert to slack channel: %s' % e.response.get('error', e))
        return e.response.data

    return response.data
