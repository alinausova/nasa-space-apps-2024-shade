"""This file offers the functions to plot a heatmap to overlay over maps."""
import folium
from branca.colormap import LinearColormap
import json

def plot_geojson_heatmap(geojson_file, output_file='heatmap.html'):
    # Load GeoJSON file
    with open(geojson_file, 'r') as f:
        data = json.load(f)

    # Extract coordinates for center of map
    coordinates = data['features'][0]['geometry']['coordinates'][0]
    center_lat = sum(coord[1] for coord in coordinates) / len(coordinates)
    center_lon = sum(coord[0] for coord in coordinates) / len(coordinates)

    # Create map
    m = folium.Map(location=[center_lat, center_lon], zoom_start=13)

    # Create color map
    colormap = LinearColormap(colors=['blue', 'green', 'yellow', 'red'],
                              vmin=0, vmax=1)

    # Add GeoJSON to map
    folium.GeoJson(
        data,
        style_function=lambda feature: {
            'fillColor': colormap(feature['properties']['shade_fraction']),
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.7,
        }
    ).add_to(m)

    # Add color map to map
    colormap.add_to(m)

    # Save map
    m.save(output_file)
    print(f"Heatmap saved as {output_file}")

if __name__ == "__main__":
    geojson_file = "testarea_12-hours.json"  # Replace with your GeoJSON file path
    plot_geojson_heatmap(geojson_file)