<script lang="ts">
    import mapboxgl, {Map} from 'mapbox-gl';
    import ShadeMap from 'mapbox-gl-shadow-simulator';
    import {onMount} from "svelte";
    import SunCalc from 'suncalc';


    let map: Map | undefined; // Type for the map object
    let mapContainer: HTMLDivElement | null = null; // Type for the container element


    mapboxgl.accessToken = import.meta.env.VITE_APP_MAPBOX_TOKEN;

    // // Initialize the map
    // const map = new mapboxgl.Map({
    //   container: 'map', // ID of the element where the map will be rendered
    //   style: 'mapbox://styles/mapbox/streets-v11', // Map style to use (you can choose from Mapbox styles or customize your own)
    //   center: [-74.5, 40], // Starting position [lng, lat]
    //   zoom: 9 // Starting zoom level
    // });
    // Initialize map when component is mounted
    onMount(() => {
        if (mapContainer) {
            map = new mapboxgl.Map({
                container: mapContainer, // HTML element reference
                style: 'mapbox://styles/mapbox/streets-v11', // Map style
                center: [-74.5, 40], // Initial center [lng, lat]
                zoom: 9 // Initial zoom level
            });

            // Optional: Add navigation and geolocation controls
            map.addControl(new mapboxgl.NavigationControl());
            map.addControl(new mapboxgl.GeolocateControl({
                positionOptions: {enableHighAccuracy: true},
                trackUserLocation: true
            }));

            const { sunrise, sunset } = SunCalc.getTimes(new Date(), lat, lng);

            map.on('load', () => {
                const shadeMap = new ShadeMap({
                    date: new Date(),    // display shadows for current date
                    color: '#e338c3',    // shade color
                    opacity: 0.7,        // opacity of shade color
                    apiKey: import.meta.env.VITE_APP_SHADEMAP_TOKEN,    // obtain from https://shademap.app/about/
                    sunExposure: {
                        enabled: true,    // enable sun exposure layer
                        startDate: new Date(Date.now() - 24 * 60 * 60 * 1000),    // start date for sun exposure calculation
                        endDate: new Date(),    // end date for sun exposure calculation
                    },
                    terrainSource: {
                        _overzoom: 18,
                        tileSize: 256,
                        maxZoom: 15,
                        getSourceUrl: ({x, y, z}) => {
                            return `https://s3.amazonaws.com/elevation-tiles-prod/terrarium/${z}/${x}/${y}.png`;
                        },
                        getElevation: ({r, g, b, a}) => {
                            return (r * 256 + g + b / 256) - 32768;
                        }

                        // tileSize: 514,
                        // maxZoom: 14,
                        // getSourceUrl: ({x, y, z}) => {
                        //     const subdomain = ['a', 'b', 'c', 'd'][(x + y) % 4];
                        //     return `https://${subdomain}.tiles.mapbox.com/raster/v1/mapbox.mapbox-terrain-dem-v1/${z}/${x}/${y}.webp?sku=101wuwGrczDtH&access_token=${import.meta.env.VITE_APP_MAPBOX_TOKEN}`;
                        // },
                        // getElevation: ({r, g, b, a}) => {
                        //     return -10000 + ((r * 256 * 256 + g * 256 + b) * .1);
                        // }

                        // tileSize: 256,       // DEM tile size
                        // maxZoom: 10, // Maximum zoom of DEM tile set
                        // _overzoom: 16, // Allow overzooming of DEM tiles
                        // getSourceUrl: ({ x, y, z }) => {
                        //   // return DEM tile url for given x,y,z coordinates
                        //   return `https://s3.amazonaws.com/elevation-tiles-prod/terrarium/${z}/${x}/${y}.png`
                        // },
                        // getElevation: ({ r, g, b, a }) => {
                        //   // return elevation in meters for a given DEM tile pixel
                        //   return (r * 256 + g + b / 256) - 32768
                        // }
                    },
                    getFeatures: async () => {
                        if (!map) return [];
                        const buildingData = map.querySourceFeatures('composite', { sourceLayer: 'building' }).filter((feature) => {
                            return feature.properties && feature.properties.underground !== "true" && (feature.properties.height || feature.properties.render_height)
                        });
                        return buildingData;
                    },
                    debug: (msg) => {
                        console.log(new Date().toISOString(), msg)
                    },
                }).addTo(map);


                // // advance shade by 1 hour
                shadeMap.setDate(new Date(Date.now()));

                // sometime later...
                // ...remove layer
                // shadeMap.remove();
            });
        }


        // Cleanup function to remove the map instance on unmount
        return () => {
            if (map) map.remove();
        };
    });

</script>


<style>
    #map {
        /*position: relative;*/
        width: 100vw;
        height: 100vh;
    }
</style>


<div id="map" bind:this={mapContainer}></div>