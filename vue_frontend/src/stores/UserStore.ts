import { defineStore } from "pinia";
import axios from "axios";
import type Topic from "@/types/Topic";
// import { deserializeTopics } from "@/types/Serializers";


export const useStoreUser = defineStore("UserStore", {
    state: () => {
        return {
            topics: {} as Record<number, Topic>,
        }
    },

    getters: {
        isAuthenticated() {
            return true;
        }
    },

    actions: {
        async fetchTopics() {
            // if (Object.keys(this.topics).length) return;
            // try {
            //     const response = await axios.get("/api/gnosis/catalog_topics"); //?format=json
            //     for (const record of deserializeTopics(response.data)) {
            //         this.topics[record.id] = record;
            //     }
            // }
            // catch (error) {
            //     console.log(error);
            // }
        },
    },

});
