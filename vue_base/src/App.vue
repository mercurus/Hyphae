<script lang="ts" setup>
    import TheNavbar from "@/components/TheNavbar.vue";
    import { useMorphStore } from "@/stores/StoreMorph";
    // import { storeToRefs } from "pinia";
    const morphStore = useMorphStore();
    morphStore.fetchMorphs();
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
