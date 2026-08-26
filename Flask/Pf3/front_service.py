from flask import Flask, jsonify
import requests

app = Flask(__name__)

DATA_SERVICE = "http://127.0.0.1:5010"

@app.route("/")
def dashboard():
    status = requests.get(f"{DATA_SERVICE}/status", timeout=3).json()
    student = requests.get(f"{DATA_SERVICE}/student", timeout=3).json()
    return jsonify({
        "boodschap": f"Hallo {student['naam']}!",
        "data_service_gezond": status["gezond"],
        "data_service_tijd": status["tijd"],
        "opleiding": student["opleiding"]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011)
