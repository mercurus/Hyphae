<script lang="ts" setup>
    import TheNavbar from "@/components/TheNavbar.vue";
    import TheToaster from "@/components/TheToaster.vue";
    import useMorphStore from "@/stores/MorphStore";
    // import { storeToRefs } from "pinia";
    
    useMorphStore().fetchMorphs();
</script>

<template>
    <div>
        <TheNavbar />
        <section class="section">
            <div class="container">
                <router-view />
            </div>
        </section>
        <TheToaster />
    </div>
</template>
