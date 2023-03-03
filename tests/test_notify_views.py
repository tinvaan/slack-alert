
import unittest

from alert.notify import app


class TestNotifyViews(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        cls.app = app.test_client()
        cls.config = app.config

    def setUp(self):
        self.url = 'http://%s:%s' % (self.config.get('ALERT_SERVICE_HOST'),
                              self.config.get('ALERT_SERVICE_PORT'))

    def test_notify(self):
        r = self.app.get(self.url + '/alert/bounced')
        self.assertEqual(r.status_code, 405)

        r = self.app.post(self.url + '/alert/bounced', json={})
        self.assertEqual(r.status_code, 400)

        r = self.app.post(self.url + '/alert/bounced', json={
            "RecordType": "Bounce",
            "MessageStream": "outbound",
            "Type": "HardBounce",
            "TypeCode": 1,
            "Name": "Hard bounce",
            "Tag": "Test",
            "Description": "The server was unable to deliver your message (ex: unknown user, mailbox not found).",
            "Email": "arthur@example.com",
            "From": "notifications@honeybadger.io",
            "BouncedAt": "2019-11-05T16:33:54.9070259Z",
        })
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.get_json(), dict)

        r = self.app.post(self.url + '/alert/bounced', json={
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
        self.assertEqual(r.status_code, 202)
        self.assertTrue(r.get_json().get('ok'))
        self.assertIsNotNone(r.get_json().get('channel'))
        self.assertIsInstance(r.get_json().get('message'), dict)


if __name__ == '__main__':
    unittest.main()
