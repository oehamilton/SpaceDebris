# src/api.py
import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import io
from pathlib import Path
import threading
import time
import os
import traceback

app = Flask(__name__)
CORS(app)

SCRIPT_DIR = Path(__file__).parent
MODEL_PATH = SCRIPT_DIR.parent / "models" / "debris_classifier.h5"

model = None
model_lock = threading.Lock()
model_loaded = False

def load_model_async():
    global model, model_loaded
    time.sleep(5)  # Delay to ensure port binding
    with model_lock:
        if not model_loaded:
            print(f"Loading model at {time.strftime('%H:%M:%S')}")
            print(f"Model path: {MODEL_PATH}, exists: {os.path.exists(MODEL_PATH)}")
            try:
                start_time = time.time()
                model = tf.keras.models.load_model(MODEL_PATH, compile=False)
                model_loaded = True
                print(f"Model loaded successfully in {time.time() - start_time:.2f} seconds at {time.strftime('%H:%M:%S')}")
                print(f"Worker initializing at {time.strftime('%H:%M:%S')}")
            except Exception as e:
                print(f"Model loading failed at {time.strftime('%H:%M:%S')}: {e}")
                model_loaded = False
            try:
                print(f"Worker ready at {time.strftime('%H:%M:%S')}")
                # Simulate worker setup to catch exceptions
                if model is not None:
                    print(f"Worker setup complete at {time.strftime('%H:%M:%S')}")
                else:
                    raise Exception("Model not available for worker")
            except Exception as e:
                print(f"Worker setup failed at {time.strftime('%H:%M:%S')}: {traceback.format_exc()}")

threading.Thread(target=load_model_async, daemon=True).start()

def get_model():
    global model, model_loaded
    with model_lock:
        if not model_loaded:
            time.sleep(1)  # Retry delay
            if not model_loaded:
                raise Exception("Model failed to load, please retry.")
        return model

def preprocess_image(image):
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize((128, 128))
    image_array = np.array(image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)
    return image_array

@app.route('/predict', methods=['POST'])
def predict():
    try:
        model = get_model()
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        file = request.files['image']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        if not (file.filename.endswith('.png') or file.filename.endswith('.jpg') or file.filename.endswith('.jpeg')):
            return jsonify({"error": "Unsupported file format. Use PNG or JPEG."}), 400
        image = Image.open(io.BytesIO(file.read()))
        image_array = preprocess_image(image)
        prediction = model.predict(image_array)[0][0]
        threshold = 0.5
        predicted_class = 1 if prediction >= threshold else 0
        return jsonify({
            "probability": float(prediction),
            "class": int(predicted_class),
            "label": "Debris" if predicted_class == 1 else "No Debris"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))  # Use $PORT or default to 5000
    print(f"Server starting at {time.strftime('%H:%M:%S')} on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)