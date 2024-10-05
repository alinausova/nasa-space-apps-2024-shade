<script lang="ts">
    import Mapbox from "./lib/Mapbox.svelte";
    import MapboxHousing from "./lib/MapboxHousing.svelte";
    import MapboxHousingHexbins from "./lib/MapboxHousingHexbins.svelte";
    import MapboxShade from "./lib/MapboxShade.svelte";
    import Delhi from "./lib/Delhi.svelte";

    // Create a store to manage the current component
    let page = 4;

    function handleAssignPage(newPage: number) {
        page=newPage;
    }
</script>

<style>
    .overlay-buttons {
        position: absolute;
        top: 10px;
        right: 10px;
        z-index: 10000;
        display: flex;
        gap: 10px;
    }
</style>

<div class="overlay-buttons">
    <button on:click={() => handleAssignPage(1)}>Show ShadowMap API</button>
<!--    <button on:click={() => handleAssignPage(1)}>Show MapboxHousing</button>-->
    <button on:click={() => handleAssignPage(2)}>Show MapboxHousingHexbins</button>
    <button on:click={() => handleAssignPage(3)}>Show Shadow Hexbins</button>
    <button on:click={() => handleAssignPage(4)}>Show Delhi</button>
</div>

{#if page === 0}
    <Mapbox />
{:else if page === 1}
    <MapboxHousing />
{:else if page === 2}
    <MapboxHousingHexbins />
{:else if page === 3}
    <MapboxShade />
{:else if page === 4}
    <Delhi />
{/if}