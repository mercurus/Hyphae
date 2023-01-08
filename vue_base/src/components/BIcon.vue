<script lang="ts" setup>
    import { defineProps } from "vue";
    defineProps<{
        icon: string;
        iconPrefix?: string;
        extraClasses?: string;
    }>();
    //yes
</script>

<template>
    <span :class="'icon ' + (extraClasses || '')">
        <i :class="(iconPrefix || 'fa fa-') + icon"></i>
    </span>
</template>
