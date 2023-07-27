<script lang="ts" setup>
    // import { defineProps } from "vue";
    import { ref, computed } from "vue";
    import useMorphStore from "@/stores/MorphStore";
    import useTopicStore from "@/stores/TopicStore";
    import BIcon from "@/components/BIcon.vue";
    import SearchCardTopic from "@/components/SearchCardTopic.vue";
    const morphStore = useMorphStore();
    const topicStore = useTopicStore();
    topicStore.fetchTopics();
    
    //search form details
    const topicName = ref("");
    const selectedMorphId = ref(0);
    const selectedMorphIcon = computed(() => {
        if (selectedMorphId.value in morphStore.morphs) {
            return morphStore.morphs[selectedMorphId.value].icon;
        }
        return "puzzle-piece";
    });

    let iconIndex = 0;
    const funIcons = ["face-laugh", "robot", "face-angry", "skull", "face-surprise", "poo", "face-sad-cry", "ghost"];
    // setInterval(function() {
    //     if (++this.iconIndex == this.funIcons.length) this.iconIndex = 0;
    // }, 2300);
</script>

<template>
    <div class="card has-background-primary">
        <div class="card-header has-background-accent">
            <span class="title has-text-primary p-2">
                <BIcon icon="globe" extraClasses="mx-3" />
                Topic Search
            </span>
        </div>
        <div class="card-content has-text-centered">
            <div class="content">
                <div class="field is-inline-block">
                    <label class="label has-text-left has-text-accent mb-0">Name</label>
                    <div class="control has-icons-left">
                        <input type="text" v-model="topicName" class="input has-text-primary" style="width: 500px" autofocus />
                        <BIcon :icon="funIcons[iconIndex]" extraClasses="is-left" />
                    </div>
                </div>
                <div class="field is-inline-block ml-3">
                    <label class="label has-text-left has-text-accent mb-0">Morph</label>
                    <div class="control has-icons-left">
                        <div class="select">
                            <select v-model="selectedMorphId" class="select has-text-primary" style="width: 200px">
                                <option value="0">Any</option>
                                <option v-for="(value, key) in morphStore.morphs" :value="key" :key="key">{{ value.name }}</option>
                            </select>
                            <BIcon :icon="selectedMorphIcon" extraClasses="is-small is-left" />
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

    <div class="columns is-multiline mt-3">
        <div v-for="topic in topicStore.topics" :key="topic.id" class="column is-one-third py-0">
            <SearchCardTopic :record="topic" />
        </div>
    </div>

</template>
