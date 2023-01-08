import { defineStore } from "pinia";
import axios from "axios";
import Morph from "@/types/Morph";

export const useMorphStore = defineStore("StoreMorph", {
    state: () => {
        return {
            morphs: {} as Record<number, Morph>,
        }
    },

    getters: {
    },

    actions: {
        async fetchMorphs() {
            try {
                const response = await axios.get("/api/gnosis/list_morphs");
                for (const record of response.data.records) {
                    this.morphs[record.id] = new Morph(record);
                }
            }
            catch (error) {
                console.log(error);
            }
        },
    },

});
