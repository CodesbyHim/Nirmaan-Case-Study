from flask import Flask, render_template, request, jsonify
from scoring import score_transcript

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/score", methods=["POST"])
def score():
    transcript = request.form.get("transcript", "")
    duration = request.form.get("duration", "")
    try:
        duration_sec = float(duration)
    except ValueError:
        return jsonify({"error": "Please provide duration in seconds as a number."}), 400

    if not transcript.strip():
        return jsonify({"error": "Transcript is empty."}), 400

    result = score_transcript(transcript, duration_sec)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
