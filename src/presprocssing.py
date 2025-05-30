import os
import cv2
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

# Configuration
DATA_DIR = Path("../data")  # Path to downloaded GeoTIFF images
OUTPUT_DIR = Path("../data/preprocessed")  # Where to save preprocessed data
IMG_SIZE = (128, 128)  # Target image size for CNN
SPLIT_RATIO = 0.2  # Train-test split ratio

def load_images_and_labels(data_dir, labels_file=None):
    """
    Load GeoTIFF images and labels from the data directory.
    If labels_file is provided, load labels from CSV; otherwise, infer from filenames.
    """
    images = []
    labels = []
    
    # Check if a labels CSV exists
    if labels_file and labels_file.exists():
        df = pd.read_csv(labels_file)
        for _, row in df.iterrows():
            img_path = data_dir / row['image_name']
            if img_path.exists():
                img = cv2.imread(str(img_path), cv2.IMREAD_COLOR)
                if img is not None:
                    images.append(img)
                    labels.append(row['debris'])  # 1 for debris, 0 for no debris
    else:
        # Load GeoTIFF images and infer labels from filenames
        for img_path in data_dir.glob("*.tif"):
            img = cv2.imread(str(img_path), cv2.IMREAD_COLOR)
            if img is not None:
                images.append(img)
                label = 1 if "debris" in img_path.stem.lower() else 0  # Placeholder
                labels.append(label)
    
    return images, labels

def preprocess_image(img, img_size=IMG_SIZE):
    """
    Preprocess a single image: resize, normalize.
    """
    # Resize image
    img = cv2.resize(img, img_size, interpolation=cv2.INTER_AREA)
    # Normalize pixel values to [0, 1]
    img = img.astype(np.float32) / 65535.0  # GEE Sentinel-2 values range 0-65535
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
    
    # Load images
    images, labels = load_images_and_labels(DATA_DIR)
    
    # Preprocess and augment
    processed_images = []
    for img in images:
        img = preprocess_image(img)
        img = augment_image(img)
        processed_images.append(img)
    
    # Convert to numpy arrays
    images = np.array(processed_images)
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