import os
import cv2
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

# Configuration
SCRIPT_DIR = Path(__file__).parent  # Directory of this script
print(f"Script directory: {SCRIPT_DIR}")    
DATA_DIR = SCRIPT_DIR.parent / "data"  # Path to downloaded GeoTIFF images
print(f"Data directory: {DATA_DIR}")    
OUTPUT_DIR = DATA_DIR / "preprocessed"  # Where to save preprocessed data
print(f"Output directory: {OUTPUT_DIR}")
# Ensure output directory exists
IMG_SIZE = (128, 128)  # Target image size for CNN
SPLIT_RATIO = 0.2  # Train-test split ratio
LABELS_FILE = DATA_DIR / 'labels.csv'  # Path to labels CSV file

def load_images_and_labels(data_dir, labels_file):
    """ 
    Load GeoTIFF images and labels from the data directory using a CSV file. 

    Args: 
        data_dir (Path): Directory containing the images. 
        labels_file (Path): Path to the CSV file with labels (columns: image_name, debris). 

    Returns: 
        images (list): List of loaded images. 
        labels (list): List of corresponding labels. 

    Raises: 
        FileNotFoundError: If the labels file doesn't exist. """

    images = []
    labels = []
    
    # Ensure the data directory exists
    if not labels_file.exists():
        raise FileNotFoundError(f"Labels file {labels_file} does not exist.")
    
    # Load labels from CSV
    df = pd.read_csv(labels_file)
    if df.empty:
        raise ValueError("Labels file is empty. Please provide a valid labels CSV.")  
          
    # Check for required columns
    if 'image_name' not in df.columns or 'debris' not in df.columns:
        raise ValueError("Labels file must contain 'image_name' and 'debris' columns.")
    
    for _, row in df.iterrows():
            img_path = data_dir / row['image_name']
            if img_path.exists():
                img = cv2.imread(str(img_path), cv2.IMREAD_COLOR)
                if img is not None:
                    images.append(img)
                    labels.append(row['debris'])  # 1 for debris, 0 for no debris
                else:
                # Load GeoTIFF images and infer labels from filenames
                    print(f"Warning: Unable to read image {img_path}. Skipping.")
            else:   
                print(f"Warning: Image file {img_path} does not exist. Skipping.")      
    
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
    print(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load images
    images, labels = load_images_and_labels(DATA_DIR, LABELS_FILE)
    if not images:
        raise ValueError("No images loaded. Check the data directory and labels file.")     
    
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

    print("Test image shape:", X_test.shape)  # Should be (1, 128, 128, 3)
    print("Test label:", y_test)  # Should be [0]

if __name__ == "__main__":
    main()