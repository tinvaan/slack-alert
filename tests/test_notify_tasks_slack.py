
import json
import pytest
import unittest

from alert.notify import app, queue
from alert.notify.tasks import slack


@pytest.mark.usefixtures('spam')
@pytest.mark.usefixtures('bounce')
class TestNotifySlack(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        cls.app = app
        cls.config = app.config

    def setUp(self):
        queue.conf.update(CELERY_ALWAYS_EAGER=True)
        self.url = 'http://%s:%s' % (self.config.get('ALERT_SERVICE_HOST'),
                                     self.config.get('ALERT_SERVICE_PORT'))

    def test_initialize(self):
        with self.app.app_context():
            client = slack.initialize()
            self.assertIsNotNone(client)
            self.assertEqual(client.token, self.config.get('SLACK_CHANNEL_BOT_TOKEN'))

    def test_content(self):
        content = slack.content(self.spam)
        self.assertIsInstance(json.loads(content), list)

        content = slack.content(self.bounce)
        self.assertIsInstance(json.loads(content), list)

    @pytest.mark.vcr
    def test_notify(self):
        with self.app.app_context():
            r = slack.notify(self.spam)
            self.assertIsNotNone(r)
            self.assertTrue(r.get('ok'))
            self.assertIsInstance(r.get('channel'), str)
            self.assertIsInstance(r.get('message'), dict)


if __name__ == '__main__':
    unittest.main()
