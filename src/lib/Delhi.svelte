<script lang="ts">
    import { onMount } from "svelte";
    import mapboxgl from "mapbox-gl";
    import geojsonPolygonsHousing from '../assets/data/delhi_housing_hexbins.json';
    import geojsonPolygonsShade from '../assets/data/delhi_12_overview_bs5_3.json';
    import type {GeoJSON} from "geojson"; // Polygons GeoJSON data

    const accessToken = import.meta.env.VITE_APP_MAPBOX_TOKEN;

    onMount(() => {
        mapboxgl.accessToken = accessToken;

        const map = new mapboxgl.Map({
            container: 'map',
            // style: 'mapbox://styles/mapbox/standard/?lightPreset=dawn',
            // style: "mapbox://styles/mapbox/standard-satellite",
            center: [77.45495972577662, 28.615176721038946],
            zoom: 12,
        });

        map.on('style.load', () => {
            map.setConfigProperty('basemap', 'lightPreset', 'dawn');
            map.setLight({
                anchor: 'map',
                color: 'orange',
                intensity: 0.9
            });
        });

        map.on('load', () => {

            // Add polygons source
            map.addSource('geojson-polygons', {
                type: 'geojson',
                data: geojsonPolygonsHousing as GeoJSON
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
                        ['get', 'avg_price_per_sqm'],
                        56, '#680000', // Low price range
                        1000, '#ff1a1a',
                        8046, '#ff9999', // High price range
                        9000, '#ffcccc'
                    ],
                    'fill-opacity': 0.7

                }
            });
            // Popup on polygons click
            map.on('click', 'polygons', (e) => {
                const properties = e.features[0].properties;
                new mapboxgl.Popup()
                    .setLngLat(e.lngLat)
                    .setHTML(`<strong>Average Price per sqm:</strong> ${properties.avg_price_per_sqm}<br><strong>Sample Size:</strong> ${properties.sample_size}`)
                    .addTo(map);
            });

            map.addSource('geojson-shade', {
                type: 'geojson',
                data: geojsonPolygonsShade as GeoJSON
            });
            // Add polygons layer
            map.addLayer({
                id: 'shade',
                type: 'fill',
                source: 'geojson-shade',
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

            map.addSource('dem', {
                'type': 'raster-dem',
                'url': 'mapbox://mapbox.mapbox-terrain-dem-v1'
            });
            map.addLayer(
                {
                    'id': 'hillshading',
                    'source': 'dem',
                    'type': 'hillshade'
                },
                // Insert below land-structure-polygon layer,
                // where hillshading sits in the Mapbox Streets style.
                'land-structure-polygon'
            );

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
