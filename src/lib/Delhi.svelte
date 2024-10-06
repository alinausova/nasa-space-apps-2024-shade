<script lang="ts">
    import {onDestroy, onMount} from "svelte";
    import mapboxgl from "mapbox-gl";
    import geojsonPolygonsHousing from '../assets/data/delhi_housing_hexbins.json';
    // shade data file were to bug for the vite build so we split them into multiple files
    import geojsonShade from '../assets/data/lower_left_average_shade_bs10.json';
    import geojsonWater from '../assets/data/output.json';
    import geojsonTemp from '../assets/data/temp_clustersize_8.json';

    import type {GeoJSON} from "geojson"; // Polygons GeoJSON data

    const accessToken = import.meta.env.VITE_APP_MAPBOX_TOKEN;

    let showBackdrop = true;

    let shadeLayers = [
        'geojsonShade',
    ]
    let layerList = [
        'polygons',
        'waterLayer',
        'tempLayer',
        ...shadeLayers
    ];

    function toggleShowLayer(layerId: string) {
        const visibility = map?.getLayoutProperty(layerId, 'visibility');
        if (visibility === 'visible') {
            map?.setLayoutProperty(layerId, 'visibility', 'none');
        } else {
            map?.setLayoutProperty(layerId, 'visibility', 'visible');
        }
    }

    function showOneLayer(layerIds: string[]) {
        layerList.forEach((layer) => {
            if (layerIds.includes(layer)) {
                map?.setLayoutProperty(layer, 'visibility', 'visible');
            } else {
                map?.setLayoutProperty(layer, 'visibility', 'none');
            }
        });
    }


    let map: mapboxgl.Map | null = null;
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
        if (!map || !zoom) {
            return;
        }
        if (spinEnabled && !userInteracting && zoom < maxSpinZoom) {
            let distancePerSecond = 360 / secondsPerRevolution;
            if (zoom > slowSpinZoom) {
                // Slow spinning at higher zooms
                const zoomDif =
                    (maxSpinZoom - zoom) / (maxSpinZoom - slowSpinZoom);
                distancePerSecond *= zoomDif;
            }
            const center = map?.getCenter();
            center.lng -= distancePerSecond;
            // Smoothly animate the map over one second.
            // When this animation is complete, it calls a 'moveend' event.
            map?.easeTo({center, duration: 875, easing: (n) => n});
        }
    }

    let dataLayersAdded = false;

    function goToNewDelhi() {
        map?.flyTo({
            center: [77.2090, 28.6139],
            zoom: 12.5,
            essential: true // this animation is considered essential with respect to prefers-reduced-motion
        });
        spinEnabled = false;
        showBackdrop = false;
        map?.setConfigProperty('basemap', 'lightPreset', 'dawn');
        if (!dataLayersAdded) {
            addDataLayers();
        }
    }

    function goToPalam() {
        map?.flyTo({
            // center: [77.051711, 28.584854],
            center: [77.049880, 28.595711],
            zoom: 13.5,
            essential: true // this animation is considered essential with respect to prefers-reduced-motion
        });
    }

    let interval: ReturnType<typeof setInterval>

    function addDataLayers() {
        dataLayersAdded = true;
        map?.addSource('geojsonTemp', {
            type: 'geojson',
            data: geojsonTemp as GeoJSON
        });
        // Add polygons layer
        map?.addLayer({
            id: 'tempLayer',
            type: 'fill',
            source: 'geojsonTemp',
            layout: {
                visibility: 'none'
            },
            paint: {
                'fill-color': [
                    'interpolate',
                    ['linear'],
                    ['get', 'raster_val'],
                    15, '#b8ddff', // Low price range
                    25, '#ebff3b',
                    28, '#e64900',
                    30, '#ff0000',
                ],
                'fill-opacity': 0.3
            }
        });

        map?.addSource('geojson-polygons', {
            type: 'geojson',
            data: geojsonPolygonsHousing as GeoJSON
        });
        // Add polygons layer
        map?.addLayer({
            id: 'polygons',
            type: 'fill',
            source: 'geojson-polygons',
            layout: {
                visibility: 'none'
            },
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

        // add shadow layers
        // shadow sources
        map?.addSource('geojsonShade', {
            type: 'geojson',
            data: geojsonShade as GeoJSON
        });
        // shadow layers
        map?.addLayer({
            id: 'geojsonShade',
            type: 'fill',
            source: 'geojsonShade',
            layout: {
                visibility: 'none'
            },
            paint: {
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

        // impervious surfaces data
        map?.addSource('geojsonWater', {
            type: 'geojson',
            data: geojsonWater as GeoJSON
        });
        // Add polygons layer
        map?.addLayer({
            id: 'waterLayer',
            type: 'fill',
            source: 'geojsonWater',
            layout: {
                visibility: 'none'
            },
            paint: {
                'fill-color': [
                    'interpolate',
                    ['linear'],
                    ['get', 'raster_val'],
                    0, '#9e6853',
                    0.25, '#ffee7f',// Low price range
                    0.33, '#1ccaff',
                    0.40, '#005acd',
                ],
                'fill-opacity': 0.3
            }
        });
    }

    function addMarkers() {
        // Create a default Marker and add it to the map.
        const marker1 = new mapboxgl.Marker({color: '#00d6cf', size: 'large'})
            .setLngLat([77.036595, 28.594181])
            .setPopup(
                new mapboxgl.Popup({offset: 25}) // Add popups
                    .setText(`Low Risk`)
            )
            .addTo(map);

        // Create a default Marker, colored black, rotated 45 degrees.
        const marker2 = new mapboxgl.Marker({color: '#ff5011', size: 'large'})
            .setLngLat([77.070226, 28.605884])
            .setPopup(
                new mapboxgl.Popup({offset: 25}) // Add popups
                    .setText(`High Risk`)
            )
            .addTo(map);

    }

    onMount(() => {
        mapboxgl.accessToken = accessToken;

        map = new mapboxgl.Map({
            container: 'map',
            center: [77.45495972577662, 28.615176721038946],
            zoom: 1,
        });

        if (!map) {
            return;
        }

        map.on('style.load', () => {
            map?.setConfigProperty('basemap', 'lightPreset', 'dusk');
            map?.setLight({
                anchor: 'map',
                color: 'orange',
                intensity: 0.9
            });
        });

        map.on('load', () => {
            interval = setInterval(spinGlobe, 875);
        });

        // Add popup functionality
        map.on('click', 'points-layer', (e) => {
            const coordinates = e.features[0].geometry.coordinates.slice();
            const description = e.features[0].properties.description;

            // Ensure that if the map is zoomed out such that multiple
            // copies of the feature are visible, the popup appears
            // over the copy being pointed to.
            while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
                coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
            }

            new mapboxgl.Popup()
                .setLngLat(coordinates)
                .setHTML(description)
                .addTo(map);
        });
    });

    // Cleanup function to remove the map when the component is destroyed
    onDestroy(() => {
        if (map) {
            map.remove();  // Properly unmounts and removes the Mapbox map
            map = null;
        }
        clearInterval(interval);
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

    .blur-background {
        backdrop-filter: blur(10px);
        background-color: rgba(255, 255, 255, 0.5);
        border-radius: 10px;
        padding: 24px;
    }

    .overlay-title {
        font-size: 12rem;
        font-weight: bold;
        color: #ffde21;
        text-transform: uppercase;
        line-height: 13rem;
        margin: 24px;
    }
    .column {
        display: flex;
        flex-direction: column;
    }

    .row {
        display: flex;
        flex-direction: row;
        gap: 10px;
        align-items: center;
    }

    .space-between {
        justify-content: space-between;
    }

    .black {
        color: #171717;
    }

    .legend-bar-housing {
        width: 100%;
        height: 8px;
        background: linear-gradient(to right, #680000, #ff1a1a, #ff9999, #ffcccc);
    }
    .legend-bar-shade {
        width: 100%;
        height: 8px;
        background: linear-gradient(to right, #e1e1e1, #7c7c7c, #353535);
    }
    .legend-bar-water {
        width: 100%;
        height: 8px;
        background: linear-gradient(to right, #9e6853, #ffee7f, #1ccaff, #005acd);
    }
    .legend-bar-temp {
        width: 100%;
        height: 8px;
        background: linear-gradient(to right, #b8ddff, #ebff3b, #e64900, #ff0000);
    }
    .legend-caption {
        font-size: 0.8rem;
        color: #353535;
    }

</style>


{#if showBackdrop}
    <div class="overlay-backdrop column">
        <h1 class="overlay-title">
            Shade for All
        </h1>
        <button on:click={goToNewDelhi}>Go to New Delhi</button>
    </div>
{:else}
    <div class="overlay-buttons column blur-background">
        <div class="row space-between">
            <span class="black">Housing data</span>
            <div class="row">
                <button on:click={() => showOneLayer(['polygons'])}>Show</button>
                <button on:click={() => toggleShowLayer('polygons')}>Toggle</button>
            </div>
        </div>
        <div class="legend-bar-housing"/>
        <div class="row space-between legend-caption"><span>Low price</span> <span>High price</span></div>
        <div class="row space-between">
            <span class="black">Shadows</span>
            <div class="row">
                <button on:click={() => showOneLayer(shadeLayers)}>
                    Show
                </button>
                <button on:click={() => {
                    shadeLayers.forEach((layer) => {
                        toggleShowLayer(layer);
                    });
            }}>Toggle
                </button>
            </div>
        </div>
        <div class="legend-bar-shade"/>
        <div class="row space-between legend-caption"><span>Low shade</span> <span>High shade</span></div>
        <div class="row space-between">
            <span class="black">Built up environment</span>
            <div class="row">
                <button on:click={() => showOneLayer(['waterLayer'])}>Show</button>
                <button on:click={() => toggleShowLayer('waterLayer')}>Toggle</button>
            </div>
        </div>
        <div class="legend-bar-water"/>
        <div class="row space-between legend-caption"><span>Artificial</span> <span>Natural</span> </div>
        <div class="row space-between">
            <span class="black">Temperature</span>
            <div class="row">
                <button on:click={() => showOneLayer(['tempLayer'])}>Show</button>
                <button on:click={() => toggleShowLayer('tempLayer')}>Toggle</button>
            </div>
        </div>
        <div class="legend-bar-temp"/>
        <div class="row space-between legend-caption"><span>Low temperature</span> <span>High temperature</span></div>
        <button on:click={goToNewDelhi}>Go to New Delhi</button>
        <button on:click={goToPalam}>Go to Palam</button>
        <button on:click={addMarkers}>Show Heat Vulnerability Index Markers</button>
    </div>
{/if}


<!-- Map Container -->
<div id="map"></div>

<div>mapbox api key is missing</div>
