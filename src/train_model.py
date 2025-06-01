import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.metrics import Precision, Recall
from tensorflow.keras.callbacks import EarlyStopping
from pathlib import Path
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score

print("TensorFlow version:", tf.__version__)

# Configuration
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data" / "preprocessed"
MODEL_DIR = SCRIPT_DIR.parent / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)
MODEL_PATH = MODEL_DIR / "debris_classifier.keras"

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

# Extremely mild data augmentation
datagen = ImageDataGenerator(
    rotation_range=30,
    width_shift_range=0.3,
    height_shift_range=0.3,
    zoom_range=0.3,
    brightness_range=[0.6, 1.4],
    shear_range=0.02,
    channel_shift_range=20,
    fill_mode='nearest'
)

# Build the CNN model
print("Building model...")
model = Sequential([
    Conv2D(8, (3, 3), activation='relu', padding='same', input_shape=(128, 128, 3)),
    BatchNormalization(),
    MaxPooling2D((2, 2)),  # Output: (64, 64, 8)
    
    Conv2D(16, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    MaxPooling2D((2, 2)),  # Output: (32, 32, 16)
    
    Conv2D(32, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    MaxPooling2D((2, 2)),  # Output: (16, 16, 32)
    
    Flatten(),  # Output: (16 * 16 * 32 = 8192)
    Dense(32, activation='relu'),
    Dropout(0.3),
    Dense(1, activation='sigmoid')
])

# Compile the model with adjusted class weights
print("Compiling model...")
class_weight = {0: 1.0, 1: 2.0}  # Kept from previous run
model.compile(
    optimizer=Adam(learning_rate=0.001),  # Reduced from 0.0005
    loss='binary_crossentropy',
    metrics=['accuracy', Precision(), Recall()]
)

# Print model summary
model.summary()

# # Early stopping callback
# early_stopping = EarlyStopping(
#     monitor='val_loss',
#     patience=10,
#     restore_best_weights=True
# )

# Train the model with extremely mild augmentation
print("Training model...")
history = model.fit(
    datagen.flow(X_train, y_train, batch_size=2),
    validation_data=(X_test, y_test),
    epochs=20,
    steps_per_epoch=len(X_train) // 2,
    class_weight=class_weight,
    #callbacks=[early_stopping],
    verbose=1
)

# Save the model
model.save(MODEL_PATH)
print(f"Model saved to {MODEL_PATH}")

# Plot training history
plt.figure(figsize=(12, 6))
plt.subplot(1, 3, 1)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

plt.subplot(1, 3, 2)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

plt.subplot(1, 3, 3)
plt.plot(history.history['precision'], label='Training Precision')
plt.plot(history.history['val_precision'], label='Validation Precision')
plt.title('Model Precision')
plt.xlabel('Epoch')
plt.ylabel('Precision')
plt.legend()

plt.tight_layout()
plt.savefig(MODEL_DIR / "training_history.png")
plt.show()

# Evaluate the model on the test set
test_loss, test_accuracy, test_precision, test_recall = model.evaluate(X_test, y_test, verbose=0)
print(f"Test Loss: {test_loss:.4f}")
print(f"Test Accuracy: {test_accuracy:.4f}")
print(f"Test Precision: {test_precision:.4f}")
print(f"Test Recall: {test_recall:.4f}")

# Find optimal threshold on validation set
predictions = model.predict(X_test)
thresholds = np.arange(0.1, 0.9, 0.1)
best_f1 = 0
best_threshold = 0.5
for threshold in thresholds:
    pred_classes = (predictions > threshold).astype(int)
    f1 = f1_score(y_test, pred_classes)
    if f1 > best_f1:
        best_f1 = f1
        best_threshold = threshold

print(f"Best threshold (maximizing F1 score): {best_threshold:.2f}, F1 Score: {best_f1:.4f}")
print("Test predictions (probabilities):", predictions)
print(f"Test predictions (classes, threshold={best_threshold:.2f}):", (predictions > best_threshold).astype(int))
print("True test labels:", y_test)

# Calculate accuracy with optimal threshold
pred_classes = (predictions > best_threshold).astype(int)
accuracy = np.mean(pred_classes.flatten() == y_test)
print(f"Test Accuracy with threshold {best_threshold:.2f}: {accuracy:.4f}")