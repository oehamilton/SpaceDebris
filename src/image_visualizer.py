# 
# This script visualizes a Sentinel-2 image tile using OpenCV.
# src/image_visualizer.py

import cv2
img = cv2.imread("data/sentinel2_image_tile_1.tif")
if img is not None:
    cv2.imshow("Sentinel-2 Tile 1", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Failed to load image")