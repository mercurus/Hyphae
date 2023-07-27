<script lang="ts" setup> 
    import { defineProps } from "vue";
    defineProps<{
        icon: string;
        extraClasses?: string;
    }>();
    //BIcon = Bulma Icon https://bulma.io/documentation/elements/icon/
</script>

<template>
    <span :class="'icon ' + (extraClasses || '')">
        <i :class="'fa fa-' + icon" />
    </span>
</template>
