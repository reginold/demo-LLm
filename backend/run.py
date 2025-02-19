from flask import Flask, request, jsonify, make_response  # Add make_response
from flask_cors import CORS
import os
import openai
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

CORS(app, 
     origins=['http://localhost:3000'],  # Explicitly specify the frontend origin
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "OPTIONS"])


# ------------------------------------------------------------------------------
# Root endpoint to confirm the backend is running
# ------------------------------------------------------------------------------
@app.route("/")
def home():
    return (
        "Welcome to the Flask backend!<br>"
        "Available endpoints:<br>"
        "/api/llm_jp_172b (POST)<br>"
        "/api/gpt4o (POST)<br>"
        "/api/llama3_405b (POST)"
    )

# ------------------------------------------------------------------------------
# 1. LLM-JP-172B model (Placeholder)
# ------------------------------------------------------------------------------
@app.route("/api/llm_jp_172b", methods=["POST"])
def llm_jp_172b():
    data = request.get_json()
    prompt = data.get("prompt", "")
    # Placeholder logic – you can integrate your actual LLM-JP-172B call here.
    result_text = f"[LLM-JP-172B placeholder response for prompt: {prompt[:50]}...]"
    return jsonify({"result": result_text})

# ------------------------------------------------------------------------------
# 2. GPT-4o model
# ------------------------------------------------------------------------------
@app.route("/api/gpt4o", methods=["POST"])
def gpt4o():
    data = request.get_json()
    prompt = data.get("prompt", "")

    try:
        completion = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
        )
        result_text = completion.choices[0].message.content
    except Exception as e:
        result_text = f"Error calling GPT-4o API: {e}"

    return jsonify({"result": result_text})

# ------------------------------------------------------------------------------
# 3. Llama3-405B model
# ------------------------------------------------------------------------------
@app.route("/api/llama3_405b", methods=["POST"])
def llama3_405b():
    data = request.get_json()
    prompt = data.get("prompt", "")
    
    client = openai.OpenAI(
            base_url="https://api.sambanova.ai/v1",
        )

    try:
        completion = client.chat.completions.create(
            model="Meta-Llama-3.1-8B-Instruct",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": prompt},
            ],
        )
        result_text = completion.choices[0].message.content
    except Exception as e:
        result_text = f"Error calling Llama3-405B API: {e}"

    return jsonify({"result": result_text})

# ------------------------------------------------------------------------------
# Flask entry point
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        print("Starting Flask server on http://localhost:5000")
        app.run(host="localhost", port=5000, debug=True)
    except Exception as e:
        print(f"Error starting server: {e}")