from flask import Flask, request, jsonify, make_response, Response, stream_with_context
from flask_cors import CORS
import os
from dotenv import load_dotenv
import openai
import logging
import time
import json
from queue import Queue, Empty
from threading import Thread

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
                "llama3": time.time(),
                "gpt4o": time.time(),
                "llm_jp": time.time()
            }
            
            # Create queues for each model's responses
            response_queues = {
                "llama3": Queue(),
                "gpt4o": Queue(),
                "llm_jp": Queue()
            }
            
            def llama3_worker():
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
                            duration = current_time - start_times["llama3"]
                            response_queues["llama3"].put((content, duration))
                except Exception as e:
                    logger.error(f"Llama3 Error: {str(e)}")
                    response_queues["llama3"].put(("ERROR", str(e)))
                finally:
                    response_queues["llama3"].put(None)  # Signal completion
            
            def gpt4o_worker():
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
                            duration = current_time - start_times["gpt4o"]
                            response_queues["gpt4o"].put((content, duration))
                except Exception as e:
                    logger.error(f"GPT4o Error: {str(e)}")
                    response_queues["gpt4o"].put(("ERROR", str(e)))
                finally:
                    response_queues["gpt4o"].put(None)  # Signal completion
            
            def llm_jp_worker():
                try:
                    words = f"[LLM-JP-172B placeholder response for prompt: {prompt[:50]}...]".split()
                    for word in words:
                        current_time = time.time()
                        duration = current_time - start_times["llm_jp"]
                        response_queues["llm_jp"].put((word + " ", duration))
                        time.sleep(0.1)
                except Exception as e:
                    logger.error(f"LLM-JP Error: {str(e)}")
                    response_queues["llm_jp"].put(("ERROR", str(e)))
                finally:
                    response_queues["llm_jp"].put(None)  # Signal completion
            
            # Start all workers in separate threads
            threads = [
                Thread(target=llama3_worker),
                Thread(target=gpt4o_worker),
                Thread(target=llm_jp_worker)
            ]
            
            for thread in threads:
                thread.daemon = True
                thread.start()
            
            # Track active models
            active_models = {"llama3", "gpt4o", "llm_jp"}
            
            while active_models:
                for model_id in list(active_models):
                    try:
                        result = response_queues[model_id].get_nowait()
                        if result is None:
                            active_models.remove(model_id)
                            continue
                            
                        content, duration = result
                        if content == "ERROR":
                            error_data = json.dumps({"error": f"Error in {model_id}: {duration}"})
                            yield f"data: {error_data}\n\n"
                            active_models.remove(model_id)
                            continue
                            
                        data = json.dumps({
                            "model": model_id,
                            "content": content,
                            "timing": {
                                "duration": duration * 1000  # Convert to milliseconds
                            }
                        })
                        yield f"data: {data}\n\n"
                    except Empty:
                        continue
                
                time.sleep(0.01)  # Small delay to prevent CPU spinning
            
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