# slack-alert

A lightweight microservice that sends a slack notification for spam payloads.

## Description

The service runs a [Flask](https://flask.palletsprojects.com) server that delegates notification actions to a [Celery](https://docs.celeryq.dev/) task queue.

Slack notifications are sent using the [Python Slack SDK](https://slack.dev/python-slack-sdk) and requires a [Slack Bot token](https://api.slack.com/authentication/token-types#bot) to be configured correctly.

### Slack Bot Token

1) Navigate to your Slack apps directory: https://api.slack.com/apps
2) Create or select an existing app.
3) Find the `Bot User OAuth Token` under the "OAuth & Permissions" tab on the left menu.

![Screenshot](./media/slack-bot-token.jpeg)

Finally, expose the above bot token in your current environment and ensure your workspace has a channel with the name specified in [config.py](./alert/config.py)

```bash
$ export SLACK_BOT_TOKEN='xoxb-<your>-<bot>-<token>'
```

## Development

1) Navigate to the project root directory and export `PYTHONPATH` to include the current project.
    ```bash
    $ export PYTHONPATH = $PYTHONPATH:$(pwd)
    ```

2) Setup a virtualenv and install requirements.
    ```
    $ mkvirtualenv -p $(which python3) notify
    $ workon notify
    $ pip install -r requirements.txt
    ```

3) Run the `Flask` server using the provided run script.
    ```bash
    (notify) $ python run.py
    * Serving Flask app 'notify'
    * Debug mode: on
    * Running on http://127.0.0.1:5050
    Press CTRL+C to quit
    * Restarting with stat
    * Debugger is active!
    * Debugger PIN: 144-933-603
    ```

4) In a new tab/shell, start the `Celery` workers for the notification task queue.
    ```bash
    $ celery --app alert.notify.queue worker


    Darwin-22.3.0-arm64-arm-64bit 2023-03-09 13:08:36

    [config]
    .> app:         notify:0x104989388
    .> transport:   redis://localhost:6379//
    .> results:     disabled://
    .> concurrency: 8 (prefork)
    .> task events: OFF (enable -E to monitor tasks in this worker)

    [queues]
    .> celery           exchange=celery(direct) key=celery

    ```

5) Make reqeusts to the API server using any HTTP client. For eg;
    ```bash
    $ curl -X POST http://127.0.0.1:5050/alert/bounced -H "Content-Type: application/json" -d '{"RecordType": "Bounce", "Type": "SpamNotification", "TypeCode": 512, "Name": "Spam notification", "Tag": "", "MessageStream": "outbound", "Description": "The message was delivered, but was either blocked by the user, or classified as spam, bulk mail, or had rejected content.", "Email": "zaphod@example.com", "From": "notifications@honeybadger.io", "BouncedAt": "2023-02-27T21:41:30Z"}' | jq .

    % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                    Dload  Upload   Total   Spent    Left  Speed
    100   646  100   260  100   386    161    239  0:00:01  0:00:01 --:--:--   401
    {
    "BouncedAt": "2023-02-27T21:41:30Z",
    "Description": "The message was delivered, but was either blocked by the user, or classified as spam, bulk mail, or had rejected content.",
    "Email": "zaphod@example.com",
    "Tag": "",
    "Type": "SpamNotification"
    }
    ```

### Running tests
Launch the test suite using [pytest](https://docs.pytest.org).
```bash
$ pytest -s

Test session starts (platform: darwin, Python 3.7.15, pytest 7.2.1, pytest-sugar 0.9.6)
rootdir: /Users/harishnavnit/Workspaces/oss/honeybadger/alert
plugins: sugar-0.9.6, recording-0.12.2
collecting ...
 tests/test_notify_tasks_slack.py ✓✓✓                        75% ███████▌
 tests/test_notify_views.py ✓                             100% ██████████


Results (0.33s):
       4 passed
```

## TODO
- [Containerize the service](https://github.com/tinvaan/slack-alert/issues/4)
- [Automated deployments](https://github.com/tinvaan/slack-alert/issues/5)
- [Generate test coverage reports](https://github.com/tinvaan/slack-alert/issues/6)
