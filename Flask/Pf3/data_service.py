from flask import Flask, jsonify
import datetime

app = Flask(__name__)

STUDENT = {
    "naam": "Nieke Karhamba Zawadi",
    "opleiding": "DevOps / DevNet Associate",
    "favoriete_onderdeel": "Ansible playbooks"
}

@app.route("/status")
def status():
    return jsonify({
        "service": "data-service",
        "tijd": datetime.datetime.now().isoformat(),
        "gezond": True
    })

@app.route("/student")
def student():
    return jsonify(STUDENT)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5010)
