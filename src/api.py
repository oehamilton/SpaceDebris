# src/api.py
import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import io
from pathlib import Path
import threading

app = Flask(__name__)
CORS(app)

SCRIPT_DIR = Path(__file__).parent
MODEL_PATH = SCRIPT_DIR.parent / "models" / "debris_classifier.h5"

model = None
model_lock = threading.Lock()

def load_model_async():
    global model
    with model_lock:
        if model is None:
            print("Loading model...")
            print(f"Model path: {MODEL_PATH}")
            try:
                model = tf.keras.models.load_model(MODEL_PATH)
                print("Model loaded successfully.")
            except Exception as e:
                print(f"Model loading failed: {e}")

# Start model loading in a background thread
threading.Thread(target=load_model_async, daemon=True).start()

def preprocess_image(image):
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize((128, 128))
    image_array = np.array(image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)
    return image_array

@app.route('/predict', methods=['POST'])
def predict():
    global model
    with model_lock:
        if model is None:
            return jsonify({"error": "Model is still loading, please try again later."}), 503
    try:
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
    app.run(host='0.0.0.0', port=5000, debug=True)
