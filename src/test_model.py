# test_model.py
import tensorflow as tf
MODEL_PATH = "models/debris_classifier.keras"
model = tf.keras.models.load_model(MODEL_PATH)
print("Model loaded successfully")