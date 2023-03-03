
import pytest
import unittest

from alert.notify import app


@pytest.mark.usefixtures('spam')
@pytest.mark.usefixtures('bounce')
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

        r = self.app.post(self.url + '/alert/bounced', json=self.bounce)
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.get_json(), dict)

        r = self.app.post(self.url + '/alert/bounced', json=self.spam)
        self.assertEqual(r.status_code, 202)
        self.assertTrue(r.get_json().get('ok'))
        self.assertIsNotNone(r.get_json().get('channel'))
        self.assertIsInstance(r.get_json().get('message'), dict)


if __name__ == '__main__':
    unittest.main()
