import os
import cv2
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

# Configuration
DATA_DIR = Path("../data")  # Path to Sentinel-2 images
OUTPUT_DIR = Path("../data/preprocessed")  # Where to save preprocessed data
IMG_SIZE = (128, 128)  # Target image size for CNN
SPLIT_RATIO = 0.2  # Train-test split ratio

def load_sentinel2_image(image_dir):
    """
    Load Sentinel-2 RGB bands (B4, B3, B2) from a .SAFE directory.
    Assumes Level-2A product with 10m resolution bands.
    """
    # Find the 10m resolution bands directory
    r10m_dir = list(image_dir.glob("GRANULE/*/IMG_DATA/R10m"))[0]
    
    # Load RGB bands (B4: red, B3: green, B2: blue)
    b4_path = next(r10m_dir.glob("*_B04_10m.jp2"))  # Red
    b3_path = next(r10m_dir.glob("*_B03_10m.jp2"))  # Green
    b2_path = next(r10m_dir.glob("*_B02_10m.jp2"))  # Blue
    
    # Read bands using OpenCV
    b4 = cv2.imread(str(b4_path), cv2.IMREAD_GRAYSCALE)
    b3 = cv2.imread(str(b3_path), cv2.IMREAD_GRAYSCALE)
    b2 = cv2.imread(str(b2_path), cv2.IMREAD_GRAYSCALE)
    
    # Stack bands into an RGB image
    img = np.stack([b4, b3, b2], axis=-1)
    return img

def preprocess_image(img, img_size=IMG_SIZE):
    """
    Preprocess a single image: resize, normalize, and convert to RGB.
    """
    # Resize image
    img = cv2.resize(img, img_size, interpolation=cv2.INTER_AREA)
    # Ensure RGB format (already in RGB from Sentinel-2 bands)
    # Normalize pixel values to [0, 1]
    img = img.astype(np.float32) / 65535.0  # Sentinel-2 Level-2A values range 0-65535
    return img

def augment_image(img):
    """
    Apply basic augmentation: random flip and rotation.
    """
    # Random horizontal flip
    if np.random.rand() > 0.5:
        img = cv2.flip(img, 1)
    # Random vertical flip
    if np.random.rand() > 0.5:
        img = cv2.flip(img, 0)
    # Random rotation (90, 180, 270 degrees)
    if np.random.rand() > 0.5:
        angle = np.random.choice([90, 180, 270])
        if angle == 90:
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        elif angle == 180:
            img = cv2.rotate(img, cv2.ROTATE_180)
        else:
            img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return img

def main():
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load images (assuming .SAFE directories in data/)
    images = []
    labels = []  # Placeholder: you'll need to label images (e.g., 1 for debris, 0 for no debris)
    
    for safe_dir in DATA_DIR.glob("S2*.SAFE"):
        img = load_sentinel2_image(safe_dir)
        img = preprocess_image(img)
        img = augment_image(img)
        images.append(img)
        # Simulate labels (replace with actual labels)
        labels.append(1 if "debris" in str(safe_dir).lower() else 0)  # Placeholder
    
    # Convert to numpy arrays
    images = np.array(images)
    labels = np.array(labels)
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        images, labels, test_size=SPLIT_RATIO, random_state=42
    )
    
    # Save preprocessed data
    np.save(OUTPUT_DIR / "X_train.npy", X_train)
    np.save(OUTPUT_DIR / "X_test.npy", X_test)
    np.save(OUTPUT_DIR / "y_train.npy", y_train)
    np.save(OUTPUT_DIR / "y_test.npy", y_test)
    
    print(f"Preprocessed {len(images)} images. Train: {len(X_train)}, Test: {len(X_test)}")

if __name__ == "__main__":
    main()