<script lang="ts">
    import {onDestroy, onMount} from "svelte";
    import mapboxgl from "mapbox-gl";
    import geojsonPolygonsHousing from '../assets/data/delhi_housing_hexbins.json';
    import geojsonPolygonsShade from '../assets/data/delhi_12_overview_bs5_3.json';
    import geojsonURAvgShade from '../assets/data/upperright_average_shade.json';
    import geojsonULAvgShade from '../assets/data/upperleft_average_shade.json';
    import geojsonLLAvgShade from '../assets/data/lowerleft_average_shade.json';
    import geojsonLRAvgShade from '../assets/data/lowerright_average_shade.json';
    import geojsonTemp from '../assets/data/output.json';
    import type {GeoJSON} from "geojson"; // Polygons GeoJSON data

    const accessToken = import.meta.env.VITE_APP_MAPBOX_TOKEN;

    let showBackdrop = true;

    let map: mapboxgl.Map | null = null;
    // center: [77.45495972577662, 28.615176721038946],

    // The following values can be changed to control rotation speed:

    // At low zooms, complete a revolution every two minutes.
    const secondsPerRevolution = 120;
    // Above zoom level 5, do not rotate.
    const maxSpinZoom = 5;
    // Rotate at intermediate speeds between zoom levels 3 and 5.
    const slowSpinZoom = 3;

    let userInteracting = false;
    let spinEnabled = true;

    function spinGlobe() {
        const zoom = map?.getZoom();
        if (spinEnabled && !userInteracting && zoom < maxSpinZoom) {
            let distancePerSecond = 360 / secondsPerRevolution;
            if (zoom > slowSpinZoom) {
                // Slow spinning at higher zooms
                const zoomDif =
                    (maxSpinZoom - zoom) / (maxSpinZoom - slowSpinZoom);
                distancePerSecond *= zoomDif;
            }
            const center = map.getCenter();
            center.lng -= distancePerSecond;
            // Smoothly animate the map over one second.
            // When this animation is complete, it calls a 'moveend' event.
            map.easeTo({ center, duration: 1000, easing: (n) => n });
        }
    }

    function goToNewDelhi() {
        map?.flyTo({
            center: [77.2090, 28.6139],
            zoom: 12,
            essential: true // this animation is considered essential with respect to prefers-reduced-motion
        });
        spinEnabled = false;
        showBackdrop = false;
    }

    onMount(() => {
        mapboxgl.accessToken = accessToken;

        map = new mapboxgl.Map({
            container: 'map',
            center: [77.45495972577662, 28.615176721038946],
            zoom: 1,
        });

        if (!map){
            return;
        }

        map.on('style.load', () => {
            map?.setConfigProperty('basemap', 'lightPreset', 'dawn');
            map?.setLight({
                anchor: 'map',
                color: 'orange',
                intensity: 0.9
            });
        });

        map.on('load', () => {
            // map?.setZoom(1)
            // spinGlobe();

            setInterval(spinGlobe, 1000);
            // Add polygons source
            map?.addSource('geojson-polygons', {
                type: 'geojson',
                data: geojsonPolygonsHousing as GeoJSON
            });
            // Add polygons layer
            map?.addLayer({
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


            // map?.addSource('geojson-shade', {
            //     type: 'geojson',
            //     data: geojsonPolygonsShade as GeoJSON
            // });
            // // Add polygons layer
            // map?.addLayer({
            //     id: 'shade',
            //     type: 'fill',
            //     source: 'geojson-shade',
            //
            //     paint: {
            //         // Create a blurred effect by using opacity and color interpolation
            //         'fill-color': [
            //             'interpolate',
            //             ['linear'],
            //             ['get', 'shade_fraction'],
            //             0, '#e1e1e1',
            //             0.01, '#7c7c7c',// Low price range
            //             0.5, '#353535',
            //         ],
            //         'fill-opacity': 0.2
            //     }
            // });

            map?.addSource('geojsonURAvgShade', {
                type: 'geojson',
                data: geojsonURAvgShade as GeoJSON
            });
            // Add polygons layer
            map?.addLayer({
                id: 'shade9hur',
                type: 'fill',
                source: 'geojsonURAvgShade',
                paint: {
                    // Create a blurred effect by using opacity and color interpolation
                    'fill-color': [
                        'interpolate',
                        ['linear'],
                        ['get', 'avg_shade_fraction'],
                        0, '#e1e1e1',
                        0.01, '#7c7c7c',// Low price range
                        0.5, '#353535',
                    ],
                    'fill-opacity': 0.3
                }
            });
            map?.addSource('geojsonULAvgShade', {
                type: 'geojson',
                data: geojsonULAvgShade as GeoJSON
            });
            // Add polygons layer
            map?.addLayer({
                id: 'shade9hul',
                type: 'fill',
                source: 'geojsonULAvgShade',
                paint: {
                    // Create a blurred effect by using opacity and color interpolation
                    'fill-color': [
                        'interpolate',
                        ['linear'],
                        ['get', 'avg_shade_fraction'],
                        0, '#e1e1e1',
                        0.01, '#7c7c7c',// Low price range
                        0.5, '#353535',
                    ],
                    'fill-opacity': 0.3
                }
            });
            map?.addSource('geojsonLRAvgShade', {
                type: 'geojson',
                data: geojsonLRAvgShade as GeoJSON
            });
            // Add polygons layer
            map?.addLayer({
                id: 'shade9hlr',
                type: 'fill',
                source: 'geojsonLRAvgShade',
                paint: {
                    // Create a blurred effect by using opacity and color interpolation
                    'fill-color': [
                        'interpolate',
                        ['linear'],
                        ['get', 'avg_shade_fraction'],
                        0, '#e1e1e1',
                        0.01, '#7c7c7c',// Low price range
                        0.5, '#353535',
                    ],
                    'fill-opacity': 0.3
                }
            });
            map?.addSource('geojsonLLAvgShade', {
                type: 'geojson',
                data: geojsonLLAvgShade as GeoJSON
            });
            // Add polygons layer
            map?.addLayer({
                id: 'shade9hll',
                type: 'fill',
                source: 'geojsonLLAvgShade',
                paint: {
                    // Create a blurred effect by using opacity and color interpolation
                    'fill-color': [
                        'interpolate',
                        ['linear'],
                        ['get', 'avg_shade_fraction'],
                        0, '#e1e1e1',
                        0.01, '#7c7c7c',// Low price range
                        0.5, '#353535',
                    ],
                    'fill-opacity': 0.3
                }
            });
            //
            map?.addSource('geojsonTemp', {
                type: 'geojson',
                data: geojsonTemp as GeoJSON
            });
            // Add polygons layer
            map?.addLayer({
                id: 'tempLayer',
                type: 'fill',
                source: 'geojsonTemp',
                paint: {
                    'fill-color': [
                        'interpolate',
                        ['linear'],
                        ['get', 'raster_val'],
                        0, '#ffae8f',
                        0.25, '#ffee7f',// Low price range
                        0.33, '#1ccaff',
                        0.40, '#005acd',
                    ],
                    'fill-opacity': 0.3
                }
            });



        });
    });

    // Cleanup function to remove the map when the component is destroyed
    onDestroy(() => {
        if (map) {
            map.remove();  // Properly unmounts and removes the Mapbox map
            map = null;
        }
    });
</script>

<style>
    #map {
        width: 100vw;
        height: 100vh; /* Adjust the height as needed */
    }
    .overlay-buttons {
        position: absolute;
        top: 10px;
        right: 10px;
        z-index: 10000;
        display: flex;
        gap: 10px;
    }
    .overlay-backdrop {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.5);
        z-index: 9999;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .overlay-title {
        font-size: 12rem;
        font-weight: bold;
        color: white;
    }
    .column {
        display: flex;
        flex-direction: column;
    }
</style>

<div class="overlay-buttons">
    <button on:click={goToNewDelhi}>Go to New Delhi</button>
</div>

{#if showBackdrop}
    <div class="overlay-backdrop column">
        <div class="overlay-title">
            Heloooo
        </div>
        <button on:click={goToNewDelhi}>Go to New Delhi</button>
    </div>
{/if}


<!-- Map Container -->
<div id="map"></div>

<div>mapbox api key is missing</div>
