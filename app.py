from flask import Flask, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Metric
REQUEST_COUNT = Counter('app_requests_total', 'Total Requests')

@app.route("/")
def home():
    REQUEST_COUNT.inc()
    return "Music Detector Running!"

# ✅ THIS IS THE IMPORTANT PART
@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
