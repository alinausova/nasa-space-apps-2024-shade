<script lang="ts">
    import {onMount} from "svelte";
    import mapboxgl, {Map} from "mapbox-gl";
    import ShadeMap from "mapbox-gl-shadow-simulator";
    import SunCalc from "suncalc";

    let map: Map;
    let shadeMap: any; // TypeScript may not have type definitions for ShadeMap, so we use `any`
    let loaderText: string = '';
    let now: Date = new Date();

    let intervalTimer: number | undefined;

    // Mapbox API key
    const mapboxToken: string = import.meta.env.VITE_APP_MAPBOX_TOKEN;

    // Handlers for control buttons
    const incrementHour = (): void => {
        now = new Date(now.getTime() + 3600000);
        shadeMap && shadeMap.setDate(now);
    };

    const decrementHour = (): void => {
        now = new Date(now.getTime() - 3600000);
        shadeMap && shadeMap.setDate(now);
    };

    const playShadeMap = (): void => {
        intervalTimer = window.setInterval(() => {
            now = new Date(now.getTime() + 60000);
            shadeMap && shadeMap.setDate(now);
        }, 100);
    };

    const stopShadeMap = (): void => {
        if (intervalTimer !== undefined) {
            window.clearInterval(intervalTimer);
        }
    };

    const toggleExposure = (event: Event): void => {
        clearInterval(intervalTimer);
        const target = event.target as HTMLInputElement;
        if (!target.checked) {
            shadeMap && shadeMap.setSunExposure(false);
        } else {
            const { lat, lng } = map.getCenter();
            const { sunrise, sunset } = SunCalc.getTimes(now, lat, lng);
            shadeMap && shadeMap.setSunExposure(true, { startDate: sunrise, endDate: sunset });
        }
    };

    // Map loaded function
    const mapLoaded = (): Promise<void> => {
        return new Promise((resolve) => {
            const checkMapLoaded = () => {
                if (!map.loaded()) {
                    return;
                }
                map.off("render", checkMapLoaded);
                resolve();
            };
            map.on("render", checkMapLoaded);
            checkMapLoaded();
        });
    };

    // Initialize the map and ShadeMap when the component mounts
    onMount(async () => {
        mapboxgl.accessToken = mapboxToken;
        map = new mapboxgl.Map({
            container: "mapid",
            center: {lng: -122.18578164139899, lat: 47.694878957368815},
            zoom: 15,
            hash: true
        });

        map.on("load", () => {
            shadeMap = new ShadeMap({
                apiKey: import.meta.env.VITE_APP_SHADEMAP_TOKEN,
                date: now,
                color: "#01112f",
                opacity: 0.7,
                terrainSource: {
                    tileSize: 514,
                    maxZoom: 14,
                    getSourceUrl: ({x, y, z}) => {
                        const subdomain = ['a', 'b', 'c', 'd'][(x + y) % 4];
                        return `https://${subdomain}.tiles.mapbox.com/raster/v1/mapbox.mapbox-terrain-dem-v1/${z}/${x}/${y}.webp?sku=101wuwGrczDtH&access_token=${mapboxToken}`;
                    },
                    getElevation: ({r, g, b, a}) => {
                        return -10000 + ((r * 256 * 256 + g * 256 + b) * .1);
                    }
                },
                getFeatures: async () => {
                   await mapLoaded();
                    const buildingData = map.querySourceFeatures("composite", {sourceLayer: "building"}).filter((feature) => {
                        return feature.properties && feature.properties.underground !== "true" && (feature.properties.height || feature.properties.render_height);
                    });
                    return buildingData;
                },
                debug: (msg: string) => console.log(new Date().toISOString(), msg)
            }).addTo(map);

            shadeMap.on("tileloaded", (loadedTiles: number, totalTiles: number) => {
                loaderText = `Loading: ${(loadedTiles / totalTiles * 100).toFixed(0)}%`;
            });
        });
    });

</script>

<style>
    #mapid {
        height: 100vh;
        width: 100vw;
    }
    .mapbox-control-time {
        padding: 20px;
        background-color: white;
    }
    #exposure-gradient-container {
        display: none;
        background-color: white;
        padding: 0 10px 5px;
    }
    #exposure-gradient {
        height: 20px;
        background-image: linear-gradient(to right, rgb(0 0 255 / 0.5), rgb(0 255 0 / 0.5), rgb(255 0 0 / 0.5));
        display: flex;
    }
    #exposure-gradient > div {
        flex: 1;
        border: 1px solid white;
        text-align: center;
        font-weight: bold;
    }
    .sidebar {
        background-color: rgb(35 55 75 / 90%);
        color: #fff;
        padding: 6px 12px;
        font-family: monospace;
        z-index: 1;
        position: absolute;
        top: 0;
        left: 0;
        margin: 12px;
        border-radius: 4px;
    }
</style>

<!-- Svelte Component Template -->
<div id="mapid"></div>
<div class="mapboxgl-control-container" style="z-index: 2000; pointer-events: auto;">
    <div class="mapboxgl-ctrl-top-left">
        <div class="mapbox-control-time">
            <button on:click={decrementHour}>-1 hour</button>
            <button on:click={incrementHour}>+1 hour</button>
            <button on:click={playShadeMap}>Play</button>
            <button on:click={stopShadeMap}>Stop</button>
            <p/>
            <label><input id="exposure" type="checkbox" on:change={toggleExposure} /> Full-day sun exposure</label>
            <span id="loader">{loaderText}</span>
        </div>
        <div id="exposure-gradient-container">
            <div>Hours of sunlight</div>
            <div id="exposure-gradient"></div>
        </div>
    </div>
</div>
