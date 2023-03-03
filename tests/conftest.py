
import pytest


@pytest.fixture(scope='module')
def vcr_config():
    return {'ignore_localhost': True, 'record_mode': 'once'}


@pytest.fixture(scope='class')
def spam(request):
    request.cls.spam = {
        "RecordType": "Bounce",
        "Type": "SpamNotification",
        "TypeCode": 512,
        "Name": "Spam notification",
        "Tag": "",
        "MessageStream": "outbound",
        "Description": "The message was delivered, but was either blocked by the user, or classified as spam, bulk mail, or had rejected content.",
        "Email": "zaphod@example.com",
        "From": "notifications@honeybadger.io",
        "BouncedAt": "2023-02-27T21:41:30Z"
    }


@pytest.fixture(scope='class')
def bounce(request):
    request.cls.bounce = {
        "RecordType": "Bounce",
        "MessageStream": "outbound",
        "Type": "HardBounce",
        "TypeCode": 1,
        "Name": "Hard bounce",
        "Tag": "Test",
        "Description": "The server was unable to deliver your message (ex: unknown user, mailbox not found).",
        "Email": "arthur@example.com",
        "From": "notifications@honeybadger.io",
        "BouncedAt": "2019-11-05T16:33:54.9070259Z"
    }