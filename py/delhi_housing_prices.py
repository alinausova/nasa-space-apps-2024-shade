import csv
import json
from typing import Dict, List
import h3
from statistics import mean
from collections import defaultdict
import numpy as np

def parse_csv(file_path: str) -> List[Dict]:
    data = []
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        print("Available columns:", reader.fieldnames)
        for row in reader:
            data.append(row)
    return data

def print_price_distribution(prices_per_sqm: List[float]):
    percentiles = [0, 10, 25, 50, 75, 90, 100]
    distribution = np.percentile(prices_per_sqm, percentiles)

    print("\nPrice per Square Meter Distribution (in local currency):")
    for p, v in zip(percentiles, distribution):
        print(f"{p}th percentile: {v:.2f}")

def create_geojson(data: List[Dict], resolution: int = 8) -> Dict:
    hex_bins = defaultdict(list)
    all_prices_per_sqm = []

    for item in data:
        try:
            longitude = float(item.get('longitude', 0))
            latitude = float(item.get('latitude', 0))
            price_per_sqm = float(item.get('Price_sqft', 0))

            hex_id = h3.geo_to_h3(latitude, longitude, resolution)
            hex_bins[hex_id].append(price_per_sqm)
            all_prices_per_sqm.append(price_per_sqm)

        except (ValueError, KeyError) as e:
            print(f"Error processing item: {item}. Error: {e}")

    print_price_distribution(all_prices_per_sqm)

    features = []
    for hex_id, prices in hex_bins.items():
        avg_price = mean(prices)
        hex_boundary = h3.h3_to_geo_boundary(hex_id)

        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[lon, lat] for lat, lon in hex_boundary]]
            },
            "properties": {
                "avg_price_per_sqm": avg_price,
                "sample_size": len(prices)
            }
        }
        features.append(feature)

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    print(f"Number of features: {len(features)}")
    return geojson

def main():
    input_file = 'delhi.csv'  # Replace with your input file path
    output_file = 'delhi_housing_hexbins.geojson'

    data = parse_csv(input_file)
    if not data:
        print("No data found in the CSV file.")
        return

    geojson_data = create_geojson(data)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(geojson_data, f, ensure_ascii=False, indent=2)

    print(f"\nGeoJSON file '{output_file}' has been created successfully.")

if __name__ == "__main__":
    main()