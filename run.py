# backend_app.py
from flask import Flask, request, jsonify
import os

# If you plan to use the openai library for GPT-4o and Llama:
# pip install openai
import openai

app = Flask(__name__)

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
    openai.api_key = os.environ.get("OPENAI_API_KEY", "")
    
    try:
        completion = openai.ChatCompletion.create(
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
    
    openai.api_key = os.environ.get("SAMBANOVA_API_KEY", "")
    openai.api_base = "https://api.sambanova.ai/v1"  # Adjust if needed

    try:
        completion = openai.ChatCompletion.create(
            model="Meta-Llama-3.1-405B-Instruct",
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
    app.run(host="localhost", port=5000, debug=True)
