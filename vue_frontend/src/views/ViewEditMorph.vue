<script lang="ts" setup>
    import { defineProps, computed, reactive } from "vue";
    import useMorphStore from "@/stores/MorphStore";
    import useToaster from "@/composables/useToaster";
    import BIcon from "@/components/BIcon.vue";
    import Morph from "@/types/Morph";
    // import { useRoute } from "vue-router";

    const morphStore = useMorphStore();
    const toaster = useToaster();

    const props = defineProps<{
        id: string;
    }>();

    const record = morphStore.morphs[props.id];
    const morphCopy: Morph = reactive(JSON.parse(JSON.stringify(record)));

    const field_types = {
        "text": "Text",
        "big_text": "Big Text",
        "number": "Number",
        "date": "Date",
    };

    const fieldCount = computed(() => {
        return morphCopy.template.fields.length;
    });

    function new_field() {
        morphCopy.template.fields.push({name:"newfield" + (fieldCount.value + 1), dataType:"text"});
    }

    function remove_field(field) {
        morphCopy.template.fields.splice(morphCopy.template.fields.indexOf(field), 1);
    }

    function saveMorph() {
        //validate
        let template_fields = {};
        for (let field of morphCopy.template.fields) {
            if (field.name in template_fields) {
                toaster.showError("All fields must have a unique name");
                return;
            }
            else {
                template_fields[field.name] = true;
            }
        }

        //save
        morphStore.saveUpdateMorph(morphCopy, () => {
            toaster.showSuccess("Morph Saved");
        });
    }
</script>

<template>
    <div class="card has-background-primary">
        <div class="card-header has-background-accent">
            <span class="title has-text-primary p-2">
                <BIcon :icon="morphCopy.icon" extraClasses="mx-3" />
                {{ morphCopy.name }}
            </span>
        </div>
        <div class="card-content" style="max-width: 800px">
            <div class="field">
                <label class="label has-text-accent mb-0">Name</label>
                <input class="input" v-model="morphCopy.name" maxlength="50" />
            </div>
            <div class="field">
                <label class="label has-text-accent mb-0">Icon</label>
                <input class="input" v-model="morphCopy.icon" maxlength="50" />
            </div>
            <div class="field">
                <label class="label has-text-accent mb-0">Summary</label>
                <textarea class="textarea" v-model="morphCopy.summary" rows="2" maxlength="200"></textarea>
            </div>
            <div class="field">
                <label class="label has-text-accent mb-0">
                    Custom Fields ({{ fieldCount }})
                    <a @click="new_field" class="ml-1">
                        <BIcon icon="plus" extraClasses="tag is-accent has-text-primary" />
                    </a>
                </label>
                <div v-for="(field, index) in morphCopy.template.fields" :key="index" class="mt-1">
                    <input type="text" v-model="field.name" />
                    <select v-model="field.dataType" class="mx-1">
                        <option v-for="(val, key) in field_types" :key="key" :value="key">{{ val }}</option>
                    </select>
                    <a @click="remove_field(field)">
                        <BIcon icon="xmark" extraClasses="tag is-danger" />
                    </a>
                </div>
            </div>
            <div class="field">
                <button type="button" class="button" @click="saveMorph">
                    <BIcon icon="check" extraClasses="mr-1" />
                    Save
                </button>
            </div>

            <div class="background-icon">
                <BIcon :icon="morphCopy.icon" extraClasses="has-text-primary-light" />
            </div>
        </div>
    </div>
</template>

<style scoped>
    .background-icon {
        position: absolute;
        right: 0;
        top: 0;
        margin: 40px 100px;
        font-size: 150px;
    }
</style>