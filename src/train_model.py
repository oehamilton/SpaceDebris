import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from pathlib import Path
import matplotlib.pyplot as plt

print("TensorFlow version:", tf.__version__)

# Configuration
SCRIPT_DIR = Path(__file__).parent  # SpaceDebris/src/
DATA_DIR = SCRIPT_DIR.parent / "data" / "preprocessed"  # SpaceDebris/data/preprocessed/
MODEL_DIR = SCRIPT_DIR.parent / "models"  # SpaceDebris/models/
MODEL_DIR.mkdir(parents=True, exist_ok=True)
MODEL_PATH = MODEL_DIR / "debris_classifier.keras"  # Use .keras format

# Load preprocessed data
print("Loading preprocessed data...")
X_train = np.load(DATA_DIR / "X_train.npy")
X_test = np.load(DATA_DIR / "X_test.npy")
y_train = np.load(DATA_DIR / "y_train.npy")
y_test = np.load(DATA_DIR / "y_test.npy")

# Verify data shapes and types
print("Training data shape:", X_train.shape)
print("Test data shape:", X_test.shape)
print("Training labels shape:", y_train.shape)
print("Training labels dtype:", y_train.dtype)
print("Training labels:", y_train)
print("Test labels shape:", y_test.shape)
print("Test labels dtype:", y_test.dtype)
print("Test labels:", y_test)

# Data augmentation
datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    zoom_range=0.2,
    brightness_range=[0.8, 1.2],
    fill_mode='nearest'
)

# Build a simpler CNN model
print("Building model...")
model = Sequential([
    Conv2D(16, (3, 3), activation='relu', padding='same', input_shape=(128, 128, 3)),
    MaxPooling2D((2, 2)),  # Output: (64, 64, 16)
    
    Conv2D(32, (3, 3), activation='relu', padding='same'),
    MaxPooling2D((2, 2)),  # Output: (32, 32, 32)
    
    Conv2D(64, (3, 3), activation='relu', padding='same'),
    MaxPooling2D((2, 2)),  # Output: (16, 16, 64)
    
    Flatten(),  # Output: (16 * 16 * 64 = 16384)
    Dense(64, activation='relu'),
    Dropout(0.3),
    Dense(1, activation='sigmoid')
])

# Compile the model
print("Compiling model...")
model.compile(
    optimizer=Adam(learning_rate=0.0001),  # Lower learning rate
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# Print model summary
model.summary()

# Train the model with data augmentation
print("Training model...")
history = model.fit(
    datagen.flow(X_train, y_train, batch_size=2),
    validation_data=(X_test, y_test),
    epochs=5,  # Fewer epochs
    steps_per_epoch=len(X_train) // 2,  # 6 images / 2 = 3 steps
    verbose=1
)

# Save the model
model.save(MODEL_PATH)
print(f"Model saved to {MODEL_PATH}")

# Plot training history
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.tight_layout()
plt.savefig(MODEL_DIR / "training_history.png")
plt.show()

# Evaluate the model on the test set
test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"Test Loss: {test_loss:.4f}")
print(f"Test Accuracy: {test_accuracy:.4f}")