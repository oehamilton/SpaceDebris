#
#
# This script downloads Sentinel-2 imagery for specified areas of interest (AOIs)
# and saves them as GeoTIFF files. It uses the Google Earth Engine (GEE) API to access the Sentinel-2 Level-2A harmonized dataset.
# Sentinel-2 Image Downloader for Space Debris Detection
# src/download_sentinel2.py
#
#


import ee                       # Ensure you have the Earth Engine Python API installed
import geemap
import requests                 # Ensure you have the requests library installed
import zipfile                  # Ensure you have the zipfile library installed
import os                       # Ensure you have the os library installed
from pathlib import Path        # Ensure you have the pathlib library installed

# Initialize GEE with your project
ee.Initialize(project='spacedebris-gee')  # Replace with your Project ID

# Define a grid of smaller AOIs (0.2° x 0.2° each)
aoi_grid = [
    [5.0, 25.0, 5.2, 25.2],  # First tile
    [5.2, 25.0, 5.4, 25.2],  # Second tile (shifted east)
    [5.0, 25.2, 5.2, 25.4],  # Third tile (shifted north)
    [5.2, 25.2, 5.4, 25.4]   # Fourth tile
]

# Define output directory
output_dir = Path("data")
output_dir.mkdir(parents=True, exist_ok=True)

# Function to download and handle the image
def download_image(image, filename, scale, region):
    url = image.getDownloadURL({
        'scale': scale,
        'region': region,
        'format': 'GEO_TIFF'
    })
    print(f"Downloading data from {url}")
    
    # Download the file
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to download: {response.status_code} - {response.text}")
        return
    
    # Save the initial response (might be a ZIP or direct TIFF)
    temp_file = filename.with_suffix('.temp')
    with open(temp_file, 'wb') as f:
        f.write(response.content)
    
    # Check if the file is a ZIP
    if zipfile.is_zipfile(temp_file):
        print("Received a ZIP file, extracting...")
        with zipfile.ZipFile(temp_file, 'r') as zip_ref:
            # Extract the first .tif file (assumes one TIFF per ZIP)
            for file_name in zip_ref.namelist():
                if file_name.endswith('.tif'):
                    zip_ref.extract(file_name, output_dir)
                    # Rename the extracted file to the desired filename
                    extracted_file = output_dir / file_name
                    extracted_file.rename(filename)
                    print(f"Extracted and renamed to {filename}")
                    break
            else:
                print("No .tif file found in ZIP")
        # Remove the temporary ZIP file
        os.remove(temp_file)
    else:
        # If not a ZIP, assume it's a direct TIFF
        os.rename(temp_file, filename)
        print(f"Downloaded directly to {filename}")

# Download each AOI
for i, coords in enumerate(aoi_grid):
    aoi = ee.Geometry.Rectangle(coords)
    
    # Load Sentinel-2 imagery (Level-2A, harmonized dataset)
    collection = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
                  .filterBounds(aoi)
                  .filterDate('2025-05-01', '2025-05-29')
                  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))
                  .sort('CLOUDY_PIXEL_PERCENTAGE')
                  .first())

    # Select RGB bands (B4: red, B3: green, B2: blue)
    image = collection.select(['B4', 'B3', 'B2'])

    # Download as GeoTIFF
    output_file = output_dir / f"sentinel2_image_tile_{i}.tif"
    download_image(image, output_file, scale=10, region=aoi)