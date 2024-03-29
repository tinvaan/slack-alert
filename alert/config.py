
import os


SLACK_CHANNEL_NAME = "#spam"
SLACK_CLIENT_ID = os.getenv('SLACK_CLIENT_ID')
SLACK_CLIENT_SCOPES = os.getenv('SLACK_OAUTH_SCOPES')
SLACK_CLIENT_SECRET = os.getenv('SLACK_CLIENT_SECRET')
SLACK_CHANNEL_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')

ALERT_SERVICE_PORT = os.getenv('ALERT_SERVICE_PORT', 5050)
ALERT_SERVICE_HOST = os.getenv('ALERT_SERVICE_HOST', '127.0.0.1')

CELERY_BROKER_URL = 'redis://@localhost'
