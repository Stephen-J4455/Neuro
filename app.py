from flask import Flask, request, jsonify, send_file
from main import NeuroAi
import io

app = Flask(__name__)
neuro_ai = NeuroAi()

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("question")
    history = request.json.get("history", [])
    file_url = request.json.get("file_url")  # Get file_url
    if not user_input:
        return jsonify({"error": "Missing 'question' in request."}), 400
    # Pass history and file_url to NeuroAi.ask
    response = neuro_ai.ask(user_input, history, file_url)
    return jsonify({"response": response})

#@app.route("/synthesize-speech", methods=["POST"])
#def synthesize_speech():
    #text = request.json.get("text")
    #if not text:
        #return jsonify({"error": "Missing 'text' in request."}), 400

    #if not neuro_ai.hf_client:
        #return jsonify({"error": "Hugging Face client not configured."}), 500

    #try:
        # You need to specify the model name here
        #model_name = "hexgrad/Kokoro-82M" # e.g., "espnet/kan-bayashi_ljspeech_vits"
        #audio = neuro_ai.hf_client.text_to_speech(text, model=model_name)
        #return send_file(io.BytesIO(audio), mimetype="audio/mpeg")
    #except Exception as e:
        #return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
