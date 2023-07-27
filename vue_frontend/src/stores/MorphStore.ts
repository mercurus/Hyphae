import { defineStore } from "pinia";
import axios from "axios";
import useAPI from "@/composables/useAPI";
import type Morph from "@/types/Morph";

const api = useAPI();
const useStoreMorph = defineStore("MorphStore", {
    state: () => {
        return {
            morphs: {} as Record<number, Morph>,
        }
    },

    getters: {
    },

    actions: {
        fetchMorphs(renew=false) {
            if (Object.keys(this.morphs).length && !renew) return;
            api.get("/api/gnosis/catalog_morphs", null, (response: any) => {
                for (const record of response.data) {
                    this.morphs[record.id] = deserializeMorph(record);
                }
            });
        },

        saveUpdateMorph(morph: Morph, callback: () => void) {
            //the ViewEditMorph component sends over a copy of the morph so that 
            //unsaved changes don't affect other parts of the site
            const original = this.morphs[morph.id];
            api.put("/api/gnosis/modify_morph/" + morph.id, serializeMorph(morph), (response: any) => {
                original.name = morph.name;
                original.summary = morph.summary;
                original.icon = morph.icon;
                original.template = morph.template;
                callback();
            });
        },
    },

});
export default useStoreMorph;


function deserializeMorph(obj: any): Morph {
    return {
        id: obj.id,
        name: obj.name,
        summary: obj.summary,
        icon: obj.icon,
        template: obj.json_data,
    }
}


function serializeMorph(morph: Morph): any {
    return {
        id: morph.id,
        name: morph.name,
        summary: morph.summary,
        icon: morph.icon,
        json_data: morph.template,
    }
}
