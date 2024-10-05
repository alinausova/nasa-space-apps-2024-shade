<script lang="ts">
    import Delhi from "./lib/Delhi.svelte";
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
    .cube-container{
        display: flex;
        flex:1
    }
</style>


<Delhi/>
