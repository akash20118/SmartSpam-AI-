from flask import Flask, render_template, request
from model import predict_message, accuracy
import pandas as pd

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    prediction = ""
    confidence = 0
    category = ""
    reasons = []
    risk = ""
    urls = []

    if request.method == "POST":

        message = request.form["message"]

        result, confidence, category, reasons, risk, urls = predict_message(message)

        if result == "spam":
            prediction = "🚨 Spam Message"
        else:
            prediction = "✅ Safe Message"

    return render_template(
        "index.html",
        prediction=prediction,
        accuracy=accuracy,
        confidence=confidence,
        category=category,
        reasons=reasons,
        risk=risk,
        urls=urls
    )


@app.route("/dashboard")
def dashboard():

    data = pd.read_csv("spam.csv")

    total = len(data)

    spam_count = len(data[data["label"] == "spam"])

    ham_count = len(data[data["label"] == "ham"])

    return render_template(
        "dashboard.html",
        total=total,
        spam_count=spam_count,
        ham_count=ham_count
    )


if __name__ == "__main__":
    app.run(debug=True)