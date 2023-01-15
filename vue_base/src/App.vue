<script lang="ts" setup>
    import TheNavbar from "@/components/TheNavbar.vue";
    import { useStoreMorph } from "@/stores/StoreMorph";
    // import { storeToRefs } from "pinia";
    const storeMorph = useStoreMorph();
    storeMorph.fetchMorphs();
</script>

<template>
    <div class="sticky_footer_wrapper">
        <TheNavbar />
        <section class="section">
            <div class="container">
                <router-view />
                <div id="toaster"></div>
            </div>
        </section>
    </div>
</template>
