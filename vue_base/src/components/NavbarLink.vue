<script lang="ts" setup>
    import { defineProps } from "vue";
    import BIcon from "@/components/BIcon.vue";
    // import { RouterLink } from "vue-router";

    defineProps({
        // ...RouterLink.props,
        to: String,
        linkText: String,
        icon: String,
        extraIconClasses: String,
    })
</script>

<template>
    <router-link custom :to="to" v-slot="{ href, navigate, isActive }">
    <!-- isExactActive, route.fullPath -->
        <a @click="navigate" :href="href" :class="'navbar-item ' + (isActive ? 'has-background-accent has-text-primary' : 'navbar-mainmenu')">
            <BIcon :icon="icon" :extraClasses="extraIconClasses"></BIcon>
            <span v-if="linkText" class="navbar-mainmenu-text logo-font ml-1">{{ linkText }}</span>
        </a>
    </router-link>
</template>
