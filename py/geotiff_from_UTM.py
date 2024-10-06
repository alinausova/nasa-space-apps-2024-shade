import rasterio
import numpy as np
from rasterio.features import shapes
from rasterio.warp import transform_geom
from pyproj import CRS
from geojson import Feature, FeatureCollection, dumps

def geotiff_to_geojson(filepath, grid_size=32):
    with rasterio.open(filepath) as src:
        data = src.read(1)  # Assuming single band raster

        print(f"Original shape: {data.shape}")
        print(f"Original bounds: {src.bounds}")
        print(f"Original CRS: {src.crs}")

        # Handle infinite and NaN values
        data = np.where(np.isinf(data) | np.isnan(data), None, data)

        # Calculate grid dimensions
        rows, cols = data.shape
        grid_rows = rows // grid_size
        grid_cols = cols // grid_size

        # Create a list to store features
        features = []

        for i in range(grid_rows):
            for j in range(grid_cols):
                # Extract grid cell data
                cell_data = data[i*grid_size:(i+1)*grid_size, j*grid_size:(j+1)*grid_size]

                # Calculate mean value for the cell, ignoring None values
                valid_data = cell_data[cell_data != None]
                cell_value = np.mean(valid_data) if len(valid_data) > 0 else None

                # Skip cells with no valid data
                if cell_value is None:
                    continue

                # Create a mask for the cell
                cell_mask = np.ones_like(cell_data, dtype=bool)

                # Calculate the transform for this cell
                cell_transform = src.transform * src.transform.translation(j*grid_size, i*grid_size)

                # Get the geometry for this cell
                for geom, _ in shapes(cell_mask.astype(np.int16), mask=cell_mask, transform=cell_transform):
                    # Reproject the geometry to WGS84 (EPSG:4326)
                    geom = transform_geom(src.crs, CRS.from_epsg(4326), geom)

                    # Create a feature
                    feature = Feature(geometry=geom, properties={'raster_val': float(cell_value)})
                    features.append(feature)

        print(f"Number of features: {len(features)}")

        # Create a FeatureCollection
        feature_collection = FeatureCollection(features)

        return dumps(feature_collection)

# Example usage
if __name__ == "__main__":
    filepath = "poverty.tif"
    grid_size = 4  # Size of each grid cell in pixels
    geojson_output = geotiff_to_geojson(filepath, grid_size)

    # Save the GeoJSON to a file
    with open("deprivation_index.geojson", "w") as f:
        f.write(geojson_output)

    print("GeoJSON file has been created.")