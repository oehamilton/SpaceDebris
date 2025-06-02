import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify
from PIL import Image
import io
import os
from pathlib import Path

app = Flask(__name__)

# Configuration
SCRIPT_DIR = Path(__file__).parent
MODEL_PATH = SCRIPT_DIR.parent / "models" / "debris_classifier.keras"

# Load the trained model
print("Loading model...")
model = tf.keras.models.load_model(MODEL_PATH)
print("Model loaded successfully.")

# Preprocess the uploaded image
def preprocess_image(image):
    # Convert image to RGB if it’s not
    if image.mode != "RGB":
        image = image.convert("RGB")
    
    # Resize to 128x128 (model input size)
    image = image.resize((128, 128))
    
    # Convert to numpy array and normalize to [0, 1]
    image_array = np.array(image) / 255.0
    
    # Expand dimensions to match model input: (1, 128, 128, 3)
    image_array = np.expand_dims(image_array, axis=0)
    
    return image_array

# API endpoint to predict debris
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Check if an image file is part of the request
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        file = request.files['image']
        
        # Validate file
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if not (file.filename.endswith('.png') or file.filename.endswith('.jpg') or file.filename.endswith('.jpeg')):
            return jsonify({"error": "Unsupported file format. Use PNG or JPEG."}), 400
        
        # Read and preprocess the image
        image = Image.open(io.BytesIO(file.read()))
        image_array = preprocess_image(image)
        
        # Make prediction
        prediction = model.predict(image_array)[0][0]  # Probability for class 1
        
        # Apply threshold (assuming 0.5, adjust if needed based on training)
        threshold = 0.5
        predicted_class = 1 if prediction >= threshold else 0
        
        # Return result as JSON
        return jsonify({
            "probability": float(prediction),
            "class": int(predicted_class),
            "label": "Debris" if predicted_class == 1 else "No Debris"
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
#
# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
# Ensure the model directory exists