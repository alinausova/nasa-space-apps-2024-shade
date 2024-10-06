"""This file offers the functions to parse a geospatial tiff file into shade percentages."""
import os
import rasterio
import numpy as np
from shapely.geometry import box, mapping
import geopandas as gpd
import glob
import matplotlib.pyplot as plt

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
    plt.xlabel('Shade Fraction')
    plt.ylabel('Frequency')
    plt.savefig(output_file)
    plt.close()

def process_geotiffs(input_directory, area_name, block_size=10, output_directory='histograms'):
    # Get all TIFF files for the given area
    tiff_files = glob.glob(os.path.join(input_directory, f"{area_name}_*.tiff"))

    if not tiff_files:
        print(f"No TIFF files found for {area_name} in {input_directory}")
        return None

    accumulated_fractions = None
    transform = None
    crs = None

    # Create output directory for histograms if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    for tiff_file in tiff_files:
        with rasterio.open(tiff_file) as src:
            raster = src.read(1)  # Read the first band
            if transform is None:
                transform = src.transform
            if crs is None:
                crs = src.crs

        fractions = calculate_shade_fraction(raster, block_size)
        shade_fractions = 1 - fractions.flatten()  # Convert to shade fraction

        # Plot histogram for this time period
        time_of_day = os.path.basename(tiff_file).split('_')[-1].split('.')[0]
        histogram_title = f"Shade Fraction Distribution - {area_name} at {time_of_day}"
        histogram_file = os.path.join(output_directory, f"{area_name}_{time_of_day}_histogram.png")
        plot_shade_fraction_histogram(shade_fractions, histogram_title, histogram_file)

        if accumulated_fractions is None:
            accumulated_fractions = fractions
        else:
            accumulated_fractions += fractions

    # Calculate average fractions
    average_fractions = accumulated_fractions / len(tiff_files)

    return average_fractions, transform, crs, len(tiff_files)

def create_geojson(average_fractions, transform, crs, block_size, output_file):
    features = []
    rows, cols = average_fractions.shape
    for y in range(rows):
        for x in range(cols):
            # Calculate the coordinates of the block
            x_min, y_max = transform * (x * block_size, y * block_size)
            x_max, y_min = transform * ((x + 1) * block_size, (y + 1) * block_size)

            # Create a polygon for the block
            polygon = box(x_min, y_min, x_max, y_max)

            # Create a feature with the polygon and shade fraction
            feature = {
                'type': 'Feature',
                'geometry': mapping(polygon),
                'properties': {
                    'shade_fraction': average_fractions[y, x]  # Convert to shade fraction (1 = no shade, 0 = full shade INVERTED NOW)
                }
            }
            features.append(feature)

    # Create a GeoDataFrame
    gdf = gpd.GeoDataFrame.from_features(features, crs=crs)

    # Save to GeoJSON
    gdf.to_file(output_file, driver='GeoJSON')

    print(f"\nCreated GeoJSON with average shade fractions: {output_file}")
    print(f"Number of polygons created: {len(gdf)}")

def main(input_directory, area_name, block_size=10):
    average_fractions, transform, crs, num_hours = process_geotiffs(input_directory, area_name, block_size)

    if average_fractions is not None:
        output_file = f"{area_name}_{num_hours}-hours.json"
        create_geojson(average_fractions, transform, crs, block_size, output_file)

        # Print distribution of average shade fractions
        print_shade_distribution(1 - average_fractions.flatten())
        print(f"\nBlock size used: {block_size}x{block_size} pixels")
        print(f"Number of time periods processed: {num_hours}")
        print(f"Histograms have been saved in the 'histograms' directory")
    else:
        print("No data to process.")

if __name__ == "__main__":
    input_directory = "testarea"  # Replace with your input directory path
    area_name = "testarea"  # Replace with your area name
    block_size = 20   # Adjust this value to control the resolution
    main(input_directory, area_name, block_size)