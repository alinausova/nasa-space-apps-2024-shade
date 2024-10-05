<script lang="ts">
    import { onMount } from "svelte";
    import mapboxgl from "mapbox-gl";
    import geojsonPoints from '../assets/data/housing_data_hexbins_rent_points.json'; // Points GeoJSON data
    import geojsonPolygons from '../assets/data/housing_data_hexbins_RENT.json';
    import type {GeoJSON} from "geojson"; // Polygons GeoJSON data

    const accessToken = import.meta.env.VITE_APP_MAPBOX_TOKEN;

    onMount(() => {
        mapboxgl.accessToken = accessToken;

        const map = new mapboxgl.Map({
            container: 'map',
            style: 'mapbox://styles/mapbox/streets-v11',
            center: [73.01264, 33.67989],
            zoom: 12
        });

        map.on('load', () => {
            // Add points source
            map.addSource('geojson-points', {
                type: 'geojson',
                data: geojsonPoints as GeoJSON
            });

            // Add polygons source
            map.addSource('geojson-polygons', {
                type: 'geojson',
                data: geojsonPolygons as GeoJSON
            });

            // Add points layer
            map.addLayer({
                id: 'points',
                type: 'circle',
                source: 'geojson-points',
                paint: {
                    'circle-radius': 8,
                    'circle-color': [
                        'interpolate',
                        ['linear'],
                        ['get', 'price_per_sqm'],
                        200, '#FF5733',
                        500, '#FFC300',
                        4000, '#DAF7A6'
                    ],
                    'circle-opacity': 0.7
                }
            });

            // Add polygons layer
            map.addLayer({
                id: 'polygons',
                type: 'fill',
                source: 'geojson-polygons',
                // paint: {
                //     'fill-color': [
                //         'interpolate',
                //         ['linear'],
                //         ['get', 'avg_price_per_sqm'],
                //         200, '#ff3333', // Low price range
                //         500, '#ff6666',
                //         // 1000, '#ff9999', // High price range
                //         4000, '#ffcccc'
                //     ],
                //     'fill-opacity': 0.5
                // }
                paint: {
                    // Create a blurred effect by using opacity and color interpolation
                    'fill-color': [
                        'interpolate',
                        ['linear'],
                        ['get', 'avg_price_per_sqm'],
                        56, '#680000', // Low price range
                        100, '#ff1a1a',
                        646, '#ff9999', // High price range
                        4000, '#ffcccc'
                    ],
                        'fill-opacity': 0.5

                }
            });

            // Optional: Add outlines to polygons
            map.addLayer({
                id: 'polygon-borders',
                type: 'line',
                source: 'geojson-polygons',
                paint: {
                    'line-color': '#000',
                    'line-width': 0
                }
            });

            // Popup on points click
            map.on('click', 'points', (e) => {
                const properties = e.features[0].properties;
                new mapboxgl.Popup()
                    .setLngLat(e.lngLat)
                    .setHTML(`<strong>Property ID:</strong> ${properties.property_id}<br><strong>Type:</strong> ${properties.property_type}<br><strong>Price per sqm:</strong> ${properties.price_per_sqm}`)
                    .addTo(map);
            });

            // Popup on polygons click
            map.on('click', 'polygons', (e) => {
                const properties = e.features[0].properties;
                new mapboxgl.Popup()
                    .setLngLat(e.lngLat)
                    .setHTML(`<strong>Average Price per sqm:</strong> ${properties.avg_price_per_sqm}<br><strong>Sample Size:</strong> ${properties.sample_size}`)
                    .addTo(map);
            });
        });
    });
</script>

<style>
    #map {
        width: 100vw;
        height: 100vh; /* Adjust the height as needed */
    }
</style>

<!-- Map Container -->
<div id="map"></div>
