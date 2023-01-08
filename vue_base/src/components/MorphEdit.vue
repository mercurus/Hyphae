<template>
    <form method="post">
        <div class="card">
            <header class="card-header has-background-primary">
                <p class="card-header-title has-text-accent is-size-3">
                    <BIcon icon="fa fa-puzzle-piece" extra_classes="mx-3" />
                    Morph Edit
                </p>
            </header>
            <div class="card-content has-text-primary p-4">
                <div class="field">
                    Name
                    <div class="control">
                        <input type="text" class="input" name="name" v-model="name" maxlength="50" />
                    </div>
                </div>
                <div class="field">
                    Icon 
                    <BIcon :icon="icon" extra_classes="is-size-4 ml-3" />
                    <div class="control">
                        <input type="text" class="input" name="icon" v-model="icon" maxlength="50" />
                    </div>
                </div>
                <div>
                    Custom Fields
                    <a @click="new_field">
                        <span class="tag is-accent has-text-primary">
                            Add
                        </span>
                    </a>
                    <div v-for="field in json_data.fields" :key="field.name" class="mt-1">
                        <input type="text" v-model="field.name" />
                        <select v-model="field.type" class="mx-1">
                            <option v-for="(val, key) in field_types" :key="key" :value="key">{{ val }}</option>
                        </select>
                        <a @click="remove_field(field)">
                            <span class="tag is-danger">
                                <BIcon icon="fa fa-xmark" extra_classes="is-small" />
                            </span>
                        </a>
                    </div>
                </div>
                <div class="control mt-5">
                    <button type="submit" class="button has-background-accent-dark">
                        <BIcon icon="fa fa-check" extra_classes="mr-1" />
                        Save
                    </button>
                </div>
            </div>
            
        </div>
        <input type="hidden" name="json_data" :value="fields_as_json" />
    </form>
    <slot>asdf</slot> <!-- CSRF token -->
</template>

<script>
    // import { reactive } from 'vue'
    import BIcon from "./BIcon";

    export default {
        components: {BIcon},
        // props: ["subject"],
        data() {
            return {
                name: "",
                icon: "",
                json_data: {},

                field_types: {
                    "text": "Text",
                    "big_text": "Big Text",
                    "number": "Number",
                    "date": "Date",
                },
            }
        },
        mounted() {
            // console.log(this);
            // let obj = JSON.parse(this.subject.replaceAll("'", "\""));
            // this.name = obj.name;
            // this.icon = obj.icon;
            // this.json_data = obj.json_data;
            // if (!this.json_data?.fields) this.json_data = {fields:[]};
        },
        computed: {
            fields_as_json() {
                return JSON.stringify(this.json_data);
            }
        },
        methods: {
            new_field() {
                let found = [0];
                let num = 0;
                while (found.length == 1) {
                    num++;
                    found = this.json_data.fields.filter(f => f.name == "newfield" + num);
                }
                this.json_data.fields.push({name:"newfield" + num, type:"text"});
            },

            remove_field(field) {
                this.json_data.fields.splice(this.json_data.fields.indexOf(field), 1);
            }
        }
    }
</script>

<style scoped>
</style>
