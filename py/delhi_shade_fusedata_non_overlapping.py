import os
import rasterio
import numpy as np
from shapely.geometry import box, mapping
import geopandas as gpd
import glob
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class QuadrantCoverage:
    def __init__(self):
        self.quadrants = {
            'upper_left': None,
            'upper_right': None,
            'lower_left': None,
            'lower_right': None
        }

    def add_quadrant(self, quadrant, lon_min, lon_max, lat_min, lat_max):
        self.quadrants[quadrant] = (lon_min, lon_max, lat_min, lat_max)

    def is_overlapping(self, quadrant, lon, lat):
        if quadrant == 'upper_left':
            return False  # First quadrant, no need to check
        elif quadrant == 'upper_right':
            ul = self.quadrants['upper_left']
            return lon < ul[1] if ul else False
        elif quadrant == 'lower_left':
            ul = self.quadrants['upper_left']
            return lat > ul[2] if ul else False
        elif quadrant == 'lower_right':
            ul = self.quadrants['upper_left']
            ur = self.quadrants['upper_right']
            ll = self.quadrants['lower_left']

            # Check if the point is in the upper left quadrant
            if ul and lon < ul[1] and lat > ul[2]:
                return True

            # Check if the point is in the upper right quadrant
            if ur and lon < ur[1] and lat > ur[2]:
                return True

            # Check if the point is in the lower left quadrant
            if ll and lon < ll[1] and lat > ll[2]:
                return True

            return False

def calculate_shade_fraction(raster, block_size):
    """Calculate the fraction of unshaded area for each block."""
    rows, cols = raster.shape
    blocks_y = rows // block_size
    blocks_x = cols // block_size

    fractions = np.zeros((blocks_y, blocks_x))

    for i in range(blocks_y):
        for j in range(blocks_x):
            block = raster[i*block_size:(i+1)*block_size, j*block_size:(j+1)*block_size]
            total_value = np.sum(block)
            max_value = 255 * block_size * block_size
            fractions[i, j] = total_value / max_value

    return fractions

# ... [Other helper functions remain unchanged] ...

def create_geojson(quadrant, avg_fractions, transform, crs, block_size, output_file, quadrant_coverage):
    features = []
    rows, cols = avg_fractions.shape
    quadrant_lon_min, quadrant_lon_max = float('inf'), float('-inf')
    quadrant_lat_min, quadrant_lat_max = float('inf'), float('-inf')

    for y in range(rows):
        for x in range(cols):
            # Calculate the actual coordinates of the block
            x_min, y_max = transform * (x * block_size, y * block_size)
            x_max, y_min = transform * ((x + 1) * block_size, (y + 1) * block_size)

            # Check if this block overlaps with previously processed quadrants
            if not quadrant_coverage.is_overlapping(quadrant, x_min, y_max):
                # Create a polygon for the block
                polygon = box(x_min, y_min, x_max, y_max)

                # Create a feature with the polygon and average shade fraction
                feature = {
                    'type': 'Feature',
                    'geometry': mapping(polygon),
                    'properties': {
                        'avg_shade_fraction': 1 - avg_fractions[y, x],  # Convert to shade fraction
                    }
                }
                features.append(feature)

                # Update quadrant bounds
                quadrant_lon_min = min(quadrant_lon_min, x_min)
                quadrant_lon_max = max(quadrant_lon_max, x_max)
                quadrant_lat_min = min(quadrant_lat_min, y_min)
                quadrant_lat_max = max(quadrant_lat_max, y_max)

    # Add this quadrant to the coverage
    if quadrant_lon_min != float('inf'):
        quadrant_coverage.add_quadrant(quadrant, quadrant_lon_min, quadrant_lon_max, quadrant_lat_min, quadrant_lat_max)

    if features:
        # Create a GeoDataFrame
        gdf = gpd.GeoDataFrame.from_features(features, crs=crs)

        # Save to GeoJSON
        gdf.to_file(output_file, driver='GeoJSON')

        print(f"\nCreated GeoJSON file: {output_file}")
        print(f"Number of polygons created: {len(gdf)}")
    else:
        print(f"\nNo non-overlapping features found for {quadrant}. GeoJSON file not created.")


def print_shade_distribution(shade_fractions):
    """Calculate and print the distribution of shade fractions."""
    percentiles = [0, 10, 25, 50, 75, 90, 100]
    distribution = np.percentile(shade_fractions, percentiles)

    print("\nShade Fraction Distribution:")
    for p, v in zip(percentiles, distribution):
        print(f"{p}th percentile: {v:.4f}")

    print(f"\nMean shade fraction: {np.mean(shade_fractions):.4f}")
    print(f"Standard deviation of shade fraction: {np.std(shade_fractions):.4f}")

def plot_shade_fraction_histogram(shade_fractions, title, output_file):
    """Plot and save a histogram of shade fractions."""
    plt.figure(figsize=(10, 6))
    plt.hist(shade_fractions, bins=30, edgecolor='black')
    plt.title(title)
    plt.xlabel('Average Shade Fraction')
    plt.ylabel('Frequency')
    plt.savefig(output_file)
    plt.close()

def process_geotiffs(input_directory, block_size=10, output_directory='histograms'):
    subdirs = ['upper_left', 'upper_right', 'lower_left', 'lower_right']

    # Get all TIFF files for each subdirectory
    tiff_files = {subdir: sorted(glob.glob(os.path.join(input_directory, subdir, "*.tiff")),
                                 key=os.path.getmtime)
                  for subdir in subdirs}

    if not all(tiff_files.values()):
        print(f"No TIFF files found in one or more subdirectories of {input_directory}")
        return None

    # Create output directory for histograms if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    subdir_fractions = {subdir: [] for subdir in subdirs}
    transforms = {}
    crss = {}

    for hour in range(len(tiff_files[subdirs[0]])):  # Assume all subdirs have the same number of files
        for subdir in subdirs:
            tiff_file = tiff_files[subdir][hour]
            with rasterio.open(tiff_file) as src:
                raster = src.read(1)  # Read the first band
                if subdir not in transforms:
                    transforms[subdir] = src.transform
                if subdir not in crss:
                    crss[subdir] = src.crs

            fractions = calculate_shade_fraction(raster, block_size)
            subdir_fractions[subdir].append(fractions)

    # Calculate average shade fractions for each subdir
    avg_subdir_fractions = {subdir: np.mean(fractions, axis=0) for subdir, fractions in subdir_fractions.items()}

    # Plot histogram for average shade fractions (using combined data from all subdirs)
    #histogram_title = f"Average Shade Fraction Distribution"
    #histogram_file = os.path.join(output_directory, f"combined_average_shade_histogram.png")
    #combined_avg_fractions = np.mean(list(avg_subdir_fractions.values()), axis=0)
    #plot_shade_fraction_histogram(1 - combined_avg_fractions.flatten(), histogram_title, histogram_file)

    return avg_subdir_fractions, transforms, crss, len(tiff_files[subdirs[0]])

def create_geojson(quadrant, avg_fractions, transform, crs, block_size, output_file, quadrant_coverage):
    features = []
    rows, cols = avg_fractions.shape
    quadrant_lon_min, quadrant_lon_max = float('inf'), float('-inf')
    quadrant_lat_min, quadrant_lat_max = float('inf'), float('-inf')

    for y in range(rows):
        for x in range(cols):
            # Calculate the actual coordinates of the block
            x_min, y_max = transform * (x * block_size, y * block_size)
            x_max, y_min = transform * ((x + 1) * block_size, (y + 1) * block_size)

            # Check if this block overlaps with previously processed quadrants
            if not quadrant_coverage.is_overlapping(quadrant, x_min, y_max):
                # Create a polygon for the block
                polygon = box(x_min, y_min, x_max, y_max)

                # Create a feature with the polygon and average shade fraction
                feature = {
                    'type': 'Feature',
                    'geometry': mapping(polygon),
                    'properties': {
                        'avg_shade_fraction': 1 - avg_fractions[y, x],  # Convert to shade fraction
                    }
                }
                features.append(feature)

                # Update quadrant bounds
                quadrant_lon_min = min(quadrant_lon_min, x_min)
                quadrant_lon_max = max(quadrant_lon_max, x_max)
                quadrant_lat_min = min(quadrant_lat_min, y_min)
                quadrant_lat_max = max(quadrant_lat_max, y_max)

    # Add this quadrant to the coverage
    if quadrant_lon_min != float('inf'):
        quadrant_coverage.add_quadrant(quadrant, quadrant_lon_min, quadrant_lon_max, quadrant_lat_min, quadrant_lat_max)

    if features:
        # Create a GeoDataFrame
        gdf = gpd.GeoDataFrame.from_features(features, crs=crs)

        # Save to GeoJSON
        gdf.to_file(output_file, driver='GeoJSON')

        print(f"\nCreated GeoJSON file: {output_file}")
        print(f"Number of polygons created: {len(gdf)}")
    else:
        print(f"\nNo non-overlapping features found for {quadrant}. GeoJSON file not created.")


def main(input_directory, block_size=10):
    avg_subdir_fractions, transforms, crss, num_hours = process_geotiffs(input_directory, block_size)

    if avg_subdir_fractions is not None:
        quadrant_coverage = QuadrantCoverage()
        all_features = []

        for subdir in ['upper_left', 'upper_right', 'lower_left', 'lower_right']:
            output_file = f"{subdir}_average_shade.json"
            create_geojson(subdir, avg_subdir_fractions[subdir], transforms[subdir], crss[subdir], block_size, output_file, quadrant_coverage)

        # Print distribution of average shade fractions for all subdirs combined
        #all_avg_fractions = np.concatenate([f.flatten() for f in avg_subdir_fractions.values()])
        #print_shade_distribution(1 - all_avg_fractions)
        print(f"\nBlock size used: {block_size}x{block_size} pixels")
        print(f"Number of time periods processed: {num_hours}")
        print(f"Histogram has been saved in the 'histograms' directory")
    else:
        print("No data to process.")

if __name__ == "__main__":
    input_directory = "fusedata"  # Replace with your input directory path
    block_size = 5   # Adjust this value to control the resolution
    main(input_directory, block_size)