import ee
import geemap

print("Initializing Earth Engine...")
# Initialize GEE
ee.Initialize(project='spacedebris-gee')

# Define AOI (e.g., a point in the Sahara Desert)

aoi = ee.Geometry.Rectangle([5.0, 25.0, 5.2, 25.2])
print(aoi.getInfo())
# Define the area of interest (AOI) for downloading Sentinel-2 imagery

# Note: Adjust the coordinates to your specific area of interest
# Initialize the Earth Engine API   

# Load Sentinel-2 imagery
collection = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
              .filterBounds(aoi)
              .filterDate('2025-05-01', '2025-05-29')
              .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))
              .sort('CLOUDY_PIXEL_PERCENTAGE')
              .first())

# Select RGB bands
image = collection.select(['B4', 'B3', 'B2'])

# Download to local directory
geemap.ee_export_image(
    image,
    filename='SpaceDebris/data/sentinel2_image.tif',
    scale=10,
    region=aoi,
    file_per_band=False
)

print("Image downloaded successfully to 'SpaceDebris/data/sentinel2_image.tif'")
# Note: Ensure that the 'SpaceDebris/data/' directory exists before running this script.   