<script lang="ts" setup>
    import { defineProps } from "vue";
    import useMorphStore from "@/stores/MorphStore";
    import useTopicStore from "@/stores/TopicStore";
    import BIcon from "@/components/BIcon.vue";
    // import Topic from "@/types/Topic";
    // import { useRoute } from "vue-router";
    const morphStore = useMorphStore();
    const topicStore = useTopicStore();

    const props = defineProps<{
        id: string;
    }>();

    const topic = topicStore.topics[props.id];
    const topicMorph = morphStore.morphs[topic.morphId];
    const computedIcon = topic.icon || topicMorph.icon || "question-circle";
</script>

<template>
    <div class="card has-background-primary">
        <div class="card-header has-background-accent">
            <span class="title has-text-primary p-2">
                <BIcon :icon="computedIcon" extraClasses="mx-3" />
                {{ topic.name }}
            </span>
        </div>
        <div class="card-content">
            <div class="background-icon">
                <BIcon :icon="computedIcon" extraClasses="has-text-primary-light" />
            </div>
            <div class="content">
                <div class="field is-inline-block">
                    <label class="label has-text-left has-text-accent mb-0">Name</label>
                    asdf
                </div>
                <div class="field is-inline-block ml-3">
                    <label class="label has-text-left has-text-accent mb-0">Morph</label>
                    <div class="control has-icons-left">
                        <div class="select">
                            <select class="select has-text-primary" style="width: 200px">
                                <option value="0">Any</option>
                            </select>
                        </div>
                    </div>
                </div>
            </div>
            <div class="block">
                <button type="button" class="button">
                    <BIcon icon="search" extraClasses="mr-1" />
                    Search
                </button>
                <button type="button" class="button ml-3">
                    <BIcon icon="plus-circle" extraClasses="mr-1" />
                    New Topic
                </button>
            </div>
        </div>
    </div>
</template>

<style scoped>
    .background-icon {
        position: absolute;
        right: 0;
        top: 0;
        margin: 40px 80px;
        font-size: 150px;
    }
</style>