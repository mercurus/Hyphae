import { defineStore } from "pinia";
import axios from "axios";
import useAPI from "@/composables/useAPI";
import type Topic from "@/types/Topic";

const api = useAPI();
const useStoreTopic = defineStore("TopicStore", {
    state: () => {
        return {
            topics: {} as Record<number, Topic>,
        }
    },

    getters: {
    },

    actions: {
        async fetchTopics() {
            if (Object.keys(this.topics).length) return;
            try {
                const response = await axios.get("/api/gnosis/catalog_topics"); //?format=json
                for (const record of response.data) {
                    this.topics[record.id] = deserializeTopic(record);
                }
            }
            catch (error) {
                console.log(error);
            }
        },

        fetchTopic(renew=false) {
            // if (Object.keys(this.morphs).length && !renew) return;
            // api.get("/api/gnosis/catalog_morphs", null, (response: any) => {
            //     for (const record of response.data) {
            //         this.morphs[record.id] = deserializeMorph(record);
            //     }
            // });
        },
    },

});
export default useStoreTopic;


function deserializeTopic(obj: any): Topic {
    return {
        id: obj.id,
        name: obj.name,
        summary: obj.summary,
        icon: obj.icon,
        jsonData: obj.json_data,
        morphId: obj.morph,
        userId: obj.user,
        createdById: obj.created_by,
        createdDate: obj.created_date
    }
}


function serializeTopic(topic: Topic): any {
    return {
        id: topic.id,
        name: topic.name,
        summary: topic.summary,
        icon: topic.icon,
        json_data: topic.jsonData,
        morph: topic.morphId,
        user: topic.userId,
        created_by: topic.createdById,
        created_date: topic.createdDate.toString()
    }
}