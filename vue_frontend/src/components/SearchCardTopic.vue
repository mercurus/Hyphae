<script lang="ts" setup>
    import { defineProps, computed } from "vue";
    import useMorphStore from "@/stores/MorphStore";
    import BIcon from "@/components/BIcon.vue";
    import type Topic from "@/types/Topic";
    import type Morph from "@/types/Morph";
    // import { useStoreTopic } from "@/stores/StoreTopic";
    const morphStore = useMorphStore();
    // const storeTopic = useStoreTopic();

    const props = defineProps<{
        record: Topic;
    }>();

    const topicMorph: Morph = morphStore.morphs[props.record.morphId];
    const computedIcon: string = props.record.icon || topicMorph.icon || "question-circle";
</script>

<template>
    <router-link custom :to="{name:'seeTopic', params:{id:record.id}}" v-slot="{ href, navigate }">
        <a @click="navigate" :href="href">
            <div class="media search-result">
                <div class="media-left search-icon-block">
                    <BIcon :icon="computedIcon" extraClasses="is-size-2 m-3" />
                    <span class="is-block is-size-7 has-text-weight-bold">{{ topicMorph.name }}</span>
                </div>
                <div class="media-content">
                    <div class="is-flex">
                        <span class="has-text-weight-bold is-flex-grow-1">{{ record.name }}</span>
                        <div class="has-text-dark pr-1 is-size-6">
                            <!-- <span class="m-0">#{{ record.id }}</span> -->
                            <BIcon :icon="topicMorph.icon" />
                        </div>
                    </div>
                    <div class="is-size-7 pr-2">
                        {{ record.summary }}
                    </div>
                </div>
            </div>
        </a>
    </router-link>
</template>
