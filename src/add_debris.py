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
    num_debris = random.randint(5, 15)  # Increased from 3-8 to 5-15
    
    for _ in range(num_debris):
        # Random position
        x = random.randint(0, width - 15)  # Adjust for larger debris
        y = random.randint(0, height - 15)
        
        # Random size (3-8 pixels)
        size = random.randint(3, 15)
        
        # Random shape (circle, rectangle, or triangle)
        shape = random.choice(['circle', 'rectangle', 'triangle'])
        
        # High-contrast color (pure white or black)
        color = random.choice([(255, 255, 255), (0, 0, 0)])  # White or black
        
        if shape == 'circle':
            cv2.circle(img, (x, y), size, color, -1)
        elif shape == 'rectangle':
            cv2.rectangle(img, (x, y), (x + size, y + size), color, -1)
        else:  # Triangle
            points = np.array([
                [x, y],
                [x + size, y],
                [x + size // 2, y + size]
            ])
            cv2.fillPoly(img, [points], color)
    
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