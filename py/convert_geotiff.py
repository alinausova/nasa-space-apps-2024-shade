import rasterio
import numpy as np
import rasterio
import numpy as np
from rasterio.features import shapes
from rasterio.warp import transform_geom
from pyproj import CRS
from geojson import Feature, FeatureCollection, dumps

def geotiff_to_geojson(filepath, pool_size=1):
    with rasterio.open(filepath) as src:
        # Read the raster data
        data = src.read(1)  # Assuming single band raster

        # Perform pooling if pool_size > 1
        if pool_size > 1:
            # Ensure data shape is divisible by pool_size
            new_shape = (data.shape[0] // pool_size * pool_size,
                         data.shape[1] // pool_size * pool_size)
            data = data[:new_shape[0], :new_shape[1]]

            # Reshape and compute mean
            data = data.reshape((new_shape[0] // pool_size, pool_size,
                                 new_shape[1] // pool_size, pool_size))
            data = data.mean(axis=(1, 3))

        # Create a mask for non-nodata values
        mask = data != src.nodata

        # Get the features with their values
        results = (
            {'properties': {'raster_val': v}, 'geometry': s}
            for i, (s, v) in enumerate(
            shapes(data, mask=mask, transform=src.transform))
        )

        # Create a list to store features
        features = []
        for result in results:
            # Reproject the geometry to WGS84 (EPSG:4326)
            geom = transform_geom(src.crs, CRS.from_epsg(4326), result['geometry'])

            # Create a feature
            feature = Feature(geometry=geom, properties=result['properties'])
            features.append(feature)

        # Create a FeatureCollection
        feature_collection = FeatureCollection(features)

        return dumps(feature_collection)

# Example usage
if __name__ == "__main__":
    filepath = "LST_Clipped.tif"
    pool_size = 5  # Change this to pool pixels (e.g., 8 for 8x8 pooling)
    geojson_output = geotiff_to_geojson(filepath, pool_size)

    # Save the GeoJSON to a file
    with open("lst_clipped.geojson", "w") as f:
        f.write(geojson_output)