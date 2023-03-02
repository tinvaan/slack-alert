
import json
import logging

from flask import current_app as app
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class Slack:

    _bot = None

    @property
    def bot(self):
        if not self._bot:
            self._bot = WebClient(token=app.config.get('SLACK_CHANNEL_BOT_TOKEN'))
        return self._bot

    def send(self, payload):
        try:
            content = json.dumps([
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": payload.get('Name')
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": "*Email:* %s" % payload.get('Email')
                        }
                    ]
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": "*When:* %s" % payload.get('BouncedAt')
                        }
                    ]
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Description:* %s" % payload.get('Description')
                    }
                }
            ])
            response = self.bot.chat_postMessage(channel=app.config.get('SLACK_CHANNEL_NAME'),
                                                 text=content, blocks=content)
        except SlackApiError as e:
            logging.error('Failed to post alert to slack channel: %s' % e.response.get('error', e))
            return e.response.data

        return response.data


slack = Slack()
