import folium
from branca.colormap import LinearColormap
import json
import os

def plot_multi_sector_heatmap(input_directory, output_file='combined_heatmap.html'):
    # List of sector names
    sectors = ['upper_left', 'upper_right', 'lower_left', 'lower_right']

    # Initialize variables to calculate map center
    total_lat, total_lon, total_coords = 0, 0, 0
    all_features = []

    # Process each sector
    for sector in sectors:
        geojson_file = os.path.join(input_directory, f"{sector}_average_shade.json")

        # Load GeoJSON file
        with open(geojson_file, 'r') as f:
            data = json.load(f)

        # Extract coordinates for center of map
        for feature in data['features']:
            coordinates = feature['geometry']['coordinates'][0]
            total_lat += sum(coord[1] for coord in coordinates)
            total_lon += sum(coord[0] for coord in coordinates)
            total_coords += len(coordinates)

        # Add features to the combined list
        all_features.extend(data['features'])

    # Calculate center of the map
    center_lat = total_lat / total_coords
    center_lon = total_lon / total_coords

    # Create map
    m = folium.Map(location=[center_lat, center_lon], zoom_start=13)

    # Create color map
    colormap = LinearColormap(colors=['blue', 'green', 'yellow', 'red'],
                              vmin=0, vmax=1)

    # Add GeoJSON features to map
    folium.GeoJson(
        {"type": "FeatureCollection", "features": all_features},
        style_function=lambda feature: {
            'fillColor': colormap(feature['properties']['avg_shade_fraction']),
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.7,
        }
    ).add_to(m)

    # Add color map to map
    colormap.add_to(m)

    # Save map
    m.save(output_file)
    print(f"Combined heatmap saved as {output_file}")

if __name__ == "__main__":
    input_directory = ""  # Replace with the directory containing your sector GeoJSON files
    plot_multi_sector_heatmap(input_directory)
