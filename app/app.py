from flask import Flask, jsonify
import socket
import time

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "application": "AI-Assisted DevOps Demo",
        "status": "running",
        "message": "DevOps pipeline is working successfully"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "hostname": socket.gethostname()
    })


@app.route("/info")
def info():
    return jsonify({
        "hostname": socket.gethostname(),
        "timestamp": time.time()
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)