from flask import Flask, request, jsonify

app = Flask(__name__)

# -------------------------
# HEALTH CHECK ENDPOINT
# -------------------------
@app.route("/health")
def health():
    return {"status": "ok", "message": "AI service is running"}


# -------------------------
# SAMPLE PREDICT ENDPOINT
# -------------------------
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    # example input handling
    text = data.get("text", "")

    # dummy prediction logic (replace with your AI model)
    result = {
        "input": text,
        "prediction": "positive"
    }

    return jsonify(result)


# -------------------------
# SAMPLE CHAT ENDPOINT
# -------------------------
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    message = data.get("message", "")

    # dummy AI response (replace with Groq / LLM logic)
    response = f"You said: {message}"

    return jsonify({
        "response": response
    })


# -------------------------
# RUN FLASK APP (IMPORTANT FOR DOCKER)
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)