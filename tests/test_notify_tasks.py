
import pytest
import unittest

from alert.notify import app
from alert.notify.tasks import slack


class TestNotifyTasks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        cls.app = app
        cls.config = app.config

    def setUp(self):
        self.url = 'http://%s:%s' % (self.config.get('ALERT_SERVICE_HOST'),
                              self.config.get('ALERT_SERVICE_PORT'))

    def test_bot(self):
        with self.app.app_context():
            self.assertIsNotNone(slack.bot)
            self.assertEqual(slack.bot.token, self.config.get('SLACK_CHANNEL_BOT_TOKEN'))

    @pytest.mark.vcr
    def test_send(self):
        with self.app.app_context():
            r = slack.send(payload={
                "RecordType": "Bounce",
                "Type": "SpamNotification",
                "TypeCode": 512,
                "Name": "Spam notification",
                "Tag": "",
                "MessageStream": "outbound",
                "Description": "The message was delivered, but was either blocked by the user, or classified as spam, bulk mail, or had rejected content.",
                "Email": "zaphod@example.com",
                "From": "notifications@honeybadger.io",
                "BouncedAt": "2023-02-27T21:41:30Z",
            })
            self.assertIsNotNone(r)
            self.assertTrue(r.get('ok'))
            self.assertIsInstance(r.get('channel'), str)
            self.assertIsInstance(r.get('message'), dict)


if __name__ == '__main__':
    unittest.main()
