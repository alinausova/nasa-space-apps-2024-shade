<script lang="ts">
    import { onMount } from "svelte";
    import mapboxgl from "mapbox-gl";
    import geojsonPolygons from '../assets/data/12_overview_bs5_5.json';
    import type {GeoJSON} from "geojson"; // Polygons GeoJSON data

    const accessToken = import.meta.env.VITE_APP_MAPBOX_TOKEN;

    onMount(() => {
        mapboxgl.accessToken = accessToken;

        const map = new mapboxgl.Map({
            container: 'map',
            // style: 'mapbox://styles/mapbox/satellite-v9',
            style: 'mapbox://styles/mapbox/streets-v11',
            center: [73.01264, 33.67989],
            zoom: 12
        });

        map.on('load', () => {

            // Add polygons source
            map.addSource('geojson-polygons', {
                type: 'geojson',
                data: geojsonPolygons as GeoJSON
            });

            // Add polygons layer
            map.addLayer({
                id: 'polygons',
                type: 'fill',
                source: 'geojson-polygons',
                paint: {
                    // Create a blurred effect by using opacity and color interpolation
                    'fill-color': [
                        'interpolate',
                        ['linear'],
                        ['get', 'shade_fraction'],
                        0, '#c3dcff',
                        0.01, '#a3bbff',// Low price range
                        0.5, '#000d35',

                    ],
                    'fill-opacity': 0.2
                }
            });

            // Optional: Add outlines to polygons
            map.addLayer({
                id: 'polygon-borders',
                type: 'line',
                source: 'geojson-polygons',
                paint: {
                    'line-color': 'transparent',
                    'line-width': 0
                }
            });

            // Popup on polygons click
            map.on('click', 'polygons', (e) => {
                const properties = e.features[0].properties;
                new mapboxgl.Popup()
                    .setLngLat(e.lngLat)
                    .setHTML(`<div><p/><strong>Shade Index:</strong><p/> ${properties.shade_fraction}</div>`)
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
