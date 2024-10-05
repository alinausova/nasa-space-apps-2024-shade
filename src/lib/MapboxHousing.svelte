<script lang="ts">
    import { onMount } from "svelte";
    import mapboxgl from "mapbox-gl";
    import geojsonData from '../assets/data/housing_data.json';
    import type {GeoJSON} from "geojson"; // Adjust the path as needed

    const accessToken = import.meta.env.VITE_APP_MAPBOX_TOKEN;

    onMount(() => {
        // Initialize Mapbox
        mapboxgl.accessToken = accessToken;

        const map = new mapboxgl.Map({
            container: 'map', // The ID of the container element
            style: 'mapbox://styles/mapbox/streets-v11', // Map style
            center: [73.01264, 33.67989], // Starting position [lng, lat]
            zoom: 12 // Starting zoom level
        });

        // Wait until the map has loaded
        map.on('load', () => {
            // Add GeoJSON source
            map.addSource('geojson-data', {
                type: 'geojson',
                data: geojsonData as GeoJSON
            });

            // Add a layer to display the GeoJSON data
            map.addLayer({
                id: 'points',
                type: 'circle', // You can use 'symbol' if you want to show markers
                source: 'geojson-data',
                paint: {
                    'circle-radius': 8,
                    'circle-color': [
                        'interpolate',
                        ['linear'],
                        ['get', 'price_per_sqm'],
                        200, '#ff3c3c', // Color for lower price range
                        1000, '#ffdb6b', // Color for medium price range
                        70000, '#45ff11'  // Color for higher price range
                    ],
                    'circle-opacity': 0.7
                }
            });

            // Optionally, add a popup for each feature
            map.on('click', 'points', (e:any) => {
                const properties = e.features[0].properties;
                new mapboxgl.Popup()
                    .setLngLat(e.lngLat)
                    .setHTML(`<strong>Property ID:</strong> ${properties.property_id}<br><strong>Type:</strong> ${properties.property_type}<br><strong>Price per sqm:</strong> ${properties.price_per_sqm}`)
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
