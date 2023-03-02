
from alert.notify import app


app.run(
    debug=True,
    port=app.config.get('ALERT_SERVICE_PORT'),
    host=app.config.get('ALERT_SERVICE_HOST')
)
