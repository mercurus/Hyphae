<script lang="ts" setup>
    import BIcon from "@/components/BIcon";
    import useToasterStore from "@/stores/ToasterStore";
    const toasterStore = useToasterStore();
</script>

<template>
    <div class="toaster">
        <div 
            v-for="toast in toasterStore.activeToast" 
            :key="toast.key" 
            :class="'toast tag is-large ' + toast.colorClass"
        >
            <BIcon :icon="toast.icon" extra-classes="mr-2" />
            {{ toast.message }}
        </div>
    </div>
</template>

<style>
    /* https://codepen.io/oliverjam/pen/KKzWJQM */
    .toaster {
        --offset: 2rem;
        position: fixed;
        left: 0;
        bottom: var(--offset);
        width: 100%;
        display: grid; 
        place-content: center;
        pointer-events: none;
    }

    .toast {
        --duration: 4000ms;
        /* pushes it down by the element's height + the space below */
        --slide-down: translateY(calc(100% + var(--offset)));
        transform: var(--slide-down);
        transition: transform;
        /* Slides up immediately, then delays for --duration, then slides down */
        animation: toast_in 700ms forwards, toast_out 400ms var(--duration) forwards;
        margin: 0.25rem;
        padding: 1.75rem 1rem;
        border: 3px solid rgba(0, 0, 0, 0.2);
    }

    @keyframes toast_in {
        to {
            transform: translateY(0);
        }
    }

    @keyframes toast_out {
        to {
            transform: var(--slide-down);
            opacity: 0;
            visibility: hidden;
        }
    }
</style>