import cv2
import numpy as np

# Load the image
img = cv2.imread("data/sentinel2_image_tile_1.tif")
if img is None:
    print("Failed to load image")
else:
    # Brighten the image
    alpha = 1.0  # Contrast control (1.0 = no change)
    beta = 50    # Brightness control (increase value to brighten, e.g., 0-100)
    brightened_img = cv2.convertScaleAbs(cv2.addWeighted(img, alpha, np.zeros(img.shape, img.dtype), 0, beta))

    # Create resizable windows
    cv2.namedWindow("Original Sentinel-2 Tile 1", cv2.WINDOW_NORMAL)
    cv2.namedWindow("Brightened Sentinel-2 Tile 1", cv2.WINDOW_NORMAL)

    # Display the original and brightened images
    cv2.imshow("Original Sentinel-2 Tile 1", img)
    cv2.imshow("Brightened Sentinel-2 Tile 1", brightened_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()