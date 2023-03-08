
import json
import logging

from flask import current_app as app
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from .. import queue


class Slack:

    _bot = None

    def __init__(self, data):
        self._bot = None
        self._data = data

    @property
    def data(self):
        return self._data

    @property
    def bot(self):
        if not self._bot:
            self._bot = WebClient(token=app.config.get('SLACK_CHANNEL_BOT_TOKEN'))
        return self._bot

    @queue.task
    def notify(self):
        content = json.dumps([
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": self.data.get('Name')
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*Email:* %s" % self.data.get('Email')
                    }
                ]
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*When:* %s" % self.data.get('BouncedAt')
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Description:* %s" % self.data.get('Description')
                }
            }
        ])

        try:
            response = self.bot.chat_postMessage(channel=app.config.get('SLACK_CHANNEL_NAME'),
                                                 text=content, blocks=content)
        except SlackApiError as e:
            logging.error('Failed to post alert to slack channel: %s' % e.response.get('error', e))
            return e.response.data

        return response.data
