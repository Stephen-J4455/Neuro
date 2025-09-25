from flask import Flask, request, jsonify
from main import NeuroAi

app = Flask(__name__)
neuro_ai = NeuroAi()

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("question")
    history = request.json.get("history", [])
    if not user_input:
        return jsonify({"error": "Missing 'question' in request."}), 400
    # Pass history to NeuroAi.ask
    response = neuro_ai.ask(user_input, history)
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(debug=True)
