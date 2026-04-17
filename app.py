from flask import Flask
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

app = Flask(__name__)

REQUEST_COUNT = Counter('app_requests_total', 'Total Requests')

@app.route("/")
def home():
    REQUEST_COUNT.inc()
    return "Music Detector Running!"

# 🔥 Attach Prometheus WSGI app (BEST PRACTICE)
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
