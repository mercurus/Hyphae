import { defineStore } from "pinia";
import axios from "axios";
import Topic from "@/types/Topic";

export const useStoreTopic = defineStore("StoreTopic", {
    state: () => {
        return {
            topics: {} as Record<number, Topic>,
        }
    },

    getters: {
    },

    actions: {
        async fetchTopics() {
            try {
                const response = await axios.get("/api/gnosis/list_topics");
                for (const record of response.data.records) {
                    this.topics[record.id] = new Topic(record);
                }
            }
            catch (error) {
                console.log(error);
            }
        },
    },

});
