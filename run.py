
from alert.notify import app
from alert.notify.views import alert

app.register_blueprint(alert)

app.run(
    debug=True,
    port=app.config.get('ALERT_SERVICE_PORT'),
    host=app.config.get('ALERT_SERVICE_HOST')
)
