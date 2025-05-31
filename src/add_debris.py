import cv2
import numpy as np
import pandas as pd
from pathlib import Path
import random

# Configuration
SCRIPT_DIR = Path(__file__).parent  # Directory of this script
DATA_DIR = SCRIPT_DIR.parent / "data"  # Path to downloaded GeoTIFF images
OUTPUT_DIR = DATA_DIR / "data_with_debris"  # Where to save preprocessed data
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LABELS_FILE = DATA_DIR / "labels.csv"

# Load labels
df = pd.read_csv(LABELS_FILE)

def add_debris_to_image(img):
    """
    Add debris-like features to an image.
    Args:
        img (numpy array): Input image (RGB, shape: (height, width, 3))
    Returns:
        numpy array: Image with debris added
    """
    height, width, _ = img.shape
    num_debris = random.randint(3, 8)  # Add 3-8 debris pieces per image
    
    for _ in range(num_debris):
        # Random position
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        
        # Random size (1-5 pixels radius)
        radius = random.randint(1, 5)
        
        # Random color (bright white/gray to contrast with sand, slight transparency)
        color = (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))  # White/gray
        
        # Draw debris as a filled circle (simulating small objects)
        cv2.circle(img, (x, y), radius, color, -1)
        
        # Add slight blur to blend with background
        img = cv2.GaussianBlur(img, (5, 5), 0)
    
    return img

# Process each image based on its label
for _, row in df.iterrows():
    img_name = row['image_name']
    label = row['debris']
    
    # Load the image
    img_path = DATA_DIR / img_name
    img = cv2.imread(str(img_path), cv2.IMREAD_COLOR)
    if img is None:
        print(f"Failed to load {img_path}")
        continue
    
    # Add debris if label is 1
    if label == 1:
        print(f"Adding debris to {img_name}")
        img = add_debris_to_image(img)
    
    # Save the image (modified or unmodified)
    output_path = OUTPUT_DIR / img_name
    cv2.imwrite(str(output_path), img)
    print(f"Saved to {output_path}")

print("Finished adding debris to images")