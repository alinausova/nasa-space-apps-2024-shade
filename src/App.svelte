<script lang="ts">
    import Delhi from "./lib/Delhi.svelte";
</script>

<style>
    .github-link {
        position: fixed;
        top: 24px;
        left: 24px;
        color: #000;
        text-decoration: none;
        cursor: pointer;
        z-index: 1000;

    }
</style>

<div class="github-link">
    <a href="https://github.com/alinausova/nasa-space-apps-2024-shade" target="_blank">
        <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" alt="GitHub stars" width="44px" height="44px">
    </a>
</div>

<Delhi/>
