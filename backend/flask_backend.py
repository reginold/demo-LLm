from flask import Flask, request, jsonify, make_response, Response, stream_with_context
from flask_cors import CORS
import os
from dotenv import load_dotenv
import openai
import logging
import time
import json

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

CORS(app, 
     origins=['http://localhost:3000'],  # Explicitly specify the frontend origin
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "OPTIONS"])

# Initialize OpenAI client
client_sn = openai.OpenAI(
        api_key=os.environ["SAMBANOVA_API_KEY"],
        base_url="https://api.sambanova.ai/v1",
    )
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
    start_time = time.time()  # Store in seconds

    def generate():
        words = f"[LLM-JP-172B placeholder response for prompt: {prompt[:50]}...]".split()
        for word in words:
            current_time = time.time()
            duration = current_time - start_time
            
            data = json.dumps({
                "model": "llm_jp", 
                "content": word + " ",
                "timing": {
                    "duration": duration * 1000  # Convert to milliseconds for frontend
                }
            })
            yield f"data: {data}\n\n"
            time.sleep(0.1)
    
    return Response(stream_with_context(generate()), mimetype='text/event-stream')

# ------------------------------------------------------------------------------
# 2. GPT-4o model
# ------------------------------------------------------------------------------
@app.route("/api/gpt4o", methods=["POST"])
def gpt4o():
    data = request.get_json()
    prompt = data.get("prompt", "")
    openai.api_key = os.environ["OPENAI_API_KEY"]
    start_time = time.time()
    
    def generate():
        try:
            completion = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                stream=True
            )
            
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    current_time = time.time()
                    content = chunk.choices[0].delta.content
                    duration = (current_time - start_time) * 1000  # Convert to milliseconds
                    
                    data = json.dumps({
                        "model": "gpt4o", 
                        "content": content,
                        "timing": {
                            "duration": duration
                        }
                    })
                    yield f"data: {data}\n\n"
        except Exception as e:
            error_data = json.dumps({"error": f"Error calling GPT-4o API: {str(e)}"})
            yield f"data: {error_data}\n\n"
    
    return Response(stream_with_context(generate()), mimetype='text/event-stream')

# ------------------------------------------------------------------------------
# 3. Llama3-405B model
# ------------------------------------------------------------------------------
@app.route("/api/llama3_405b", methods=["POST"])
def llama3_405b():
    data = request.get_json()
    prompt = data.get("prompt", "")
    start_time = time.time()
    
    def generate():
        try:
            completion = client_sn.chat.completions.create(
                model="Meta-Llama-3.1-405B-Instruct",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant"},
                    {"role": "user", "content": prompt},
                ],
                stream=True
            )
            
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    current_time = time.time()
                    content = chunk.choices[0].delta.content
                    duration = (current_time - start_time) * 1000  # Convert to milliseconds
                    
                    data = json.dumps({
                        "model": "llama3", 
                        "content": content,
                        "timing": {
                            "duration": duration
                        }
                    })
                    yield f"data: {data}\n\n"
        except Exception as e:
            error_data = json.dumps({"error": f"Error calling Llama3-405B API: {str(e)}"})
            yield f"data: {error_data}\n\n"
    
    return Response(stream_with_context(generate()), mimetype='text/event-stream')

# ------------------------------------------------------------------------------
# Compare models endpoint
# ------------------------------------------------------------------------------
@app.route("/api/compare", methods=["POST"])
def compare_models():
    data = request.get_json()
    prompt = data.get("prompt", "")
    
    def generate():
        try:
            start_times = {
                "llama3": time.time(),  # Store in seconds
                "gpt4o": time.time(),
                "llm_jp": time.time()
            }
            
            # Start all three model calls concurrently
            llama_completion = client_sn.chat.completions.create(
                model="Meta-Llama-3.1-405B-Instruct",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant"},
                    {"role": "user", "content": prompt},
                ],
                stream=True
            )
            
            gpt4o_completion = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                stream=True
            )
            
            # Create generators for each model
            responses = {
                "llama3": "",
                "gpt4o": "",
                "llm_jp": ""
            }
            
            # Simulate LLM-JP streaming
            words = f"[LLM-JP-172B placeholder response for prompt: {prompt[:50]}...]".split()
            for word in words:
                current_time = time.time()
                responses["llm_jp"] += word + " "
                duration = current_time - start_times["llm_jp"]
                
                data = json.dumps({
                    "model": "llm_jp", 
                    "content": word + " ",
                    "timing": {
                        "duration": duration * 1000  # Convert to milliseconds for frontend
                    }
                })
                yield f"data: {data}\n\n"
                time.sleep(0.1)
            
            # Process Llama3 stream
            for llama_chunk in llama_completion:
                if llama_chunk.choices[0].delta.content:
                    current_time = time.time()
                    content = llama_chunk.choices[0].delta.content
                    responses["llama3"] += content
                    duration = current_time - start_times["llama3"]
                    
                    data = json.dumps({
                        "model": "llama3", 
                        "content": content,
                        "timing": {
                            "duration": duration * 1000  # Convert to milliseconds for frontend
                        }
                    })
                    yield f"data: {data}\n\n"
            
            # Process GPT4o stream
            for gpt4o_chunk in gpt4o_completion:
                if gpt4o_chunk.choices[0].delta.content:
                    current_time = time.time()
                    content = gpt4o_chunk.choices[0].delta.content
                    responses["gpt4o"] += content
                    duration = current_time - start_times["gpt4o"]
                    
                    data = json.dumps({
                        "model": "gpt4o", 
                        "content": content,
                        "timing": {
                            "duration": duration * 1000  # Convert to milliseconds for frontend
                        }
                    })
                    yield f"data: {data}\n\n"
                    
        except Exception as e:
            logger.error(f"Error in compare_models: {str(e)}")
            error_data = json.dumps({"error": str(e)})
            yield f"data: {error_data}\n\n"
    
    return Response(stream_with_context(generate()), mimetype='text/event-stream')

# ------------------------------------------------------------------------------
# Flask entry point
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        print("Starting Flask server on http://localhost:5000")
        app.run(host="localhost", port=5000)
    except Exception as e:
        print(f"Error starting server: {e}")