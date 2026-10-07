import random
import time

from flask import Flask, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

app = Flask(__name__)

REQUESTS = Counter("app_requests_total", "Total requests", ["endpoint", "status"])
LATENCY = Histogram("app_request_duration_seconds", "Request latency in seconds", ["endpoint"])


@app.route("/")
def index():
    with LATENCY.labels("/").time():
        REQUESTS.labels("/", "200").inc()
        return "Hello from the monitored app\n"


@app.route("/slow")
def slow():
    with LATENCY.labels("/slow").time():
        time.sleep(random.uniform(0.2, 1.5))
        REQUESTS.labels("/slow", "200").inc()
        return "That was slow\n"


@app.route("/error")
def error():
    with LATENCY.labels("/error").time():
        REQUESTS.labels("/error", "500").inc()
        return "Something broke\n", 500


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
