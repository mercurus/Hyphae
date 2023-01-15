<script lang="ts" setup>
    import { defineProps, computed, getCurrentInstance } from "vue";
    import { useRoute } from "vue-router";
    import { useStoreMorph } from "@/stores/StoreMorph";
    import BIcon from "@/components/BIcon.vue";
    import Topic from "@/types/Topic";
    import { useStoreTopic } from "@/stores/StoreTopic";
    const storeMorph = useStoreMorph();
    const storeTopic = useStoreTopic();


    const topic = computed(() => {
        // eslint-disable-next-line
        return storeTopic.topics[useRoute().params.id];
    });

    const topicMorph = computed(() => {
        return storeMorph.morphs[topic.value.morphId];
    });

    const computedIcon = computed(() => {
        return topic.value.icon || topicMorph.value.icon || "question-circle";
    });
    
</script>

<template>
    <div class="card has-background-primary">
        <div class="card-header has-background-accent">
            <span class="title has-text-primary p-2">
                <BIcon :icon="computedIcon" extraClasses="mx-3" />
                {{ topic.name }}
            </span>
        </div>
        <div class="card-content has-text-centered">
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
