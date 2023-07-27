<script lang="ts" setup>
    // import { defineProps } from "vue";
    import { ref, computed } from "vue";
    import useMorphStore from "@/stores/MorphStore";
    import BIcon from "@/components/BIcon.vue";
    import SearchCardMorph from "@/components/SearchCardMorph.vue";
    const morphStore = useMorphStore();
</script>

<template>
    <div class="card has-background-primary">
        <div class="card-header has-background-accent">
            <span class="title has-text-primary p-2">
                <BIcon icon="puzzle-piece" extraClasses="mx-3" />
                Morph Search
            </span>
        </div>
        <div class="card-content has-text-centered">
            <!-- <div class="content">
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
                                <option v-for="(value, key) in storeMorph.morphs" :value="key" :key="key">{{ value.name }}</option>
                            </select>
                            <BIcon :icon="selectedMorphIcon" extraClasses="is-small is-left" />
                        </div>
                    </div>
                </div>
            </div> -->
            <div class="block">
                <button type="button" class="button">
                    <BIcon icon="search" extraClasses="mr-1" />
                    Search
                </button>
                <button type="button" class="button ml-3">
                    <BIcon icon="plus-circle" extraClasses="mr-1" />
                    New Morph
                </button>
            </div>
        </div>
    </div>

    <div class="columns is-multiline mt-3">
        <div v-for="morph in morphStore.morphs" :key="morph.id" class="column is-one-third py-0">
            <SearchCardMorph :record="morph" />
        </div>
    </div>

</template>
