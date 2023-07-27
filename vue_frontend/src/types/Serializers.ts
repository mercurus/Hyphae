import type Topic from "@/types/Topic";
import type Morph from "@/types/Morph";


export function csrfHeader(): any {
    return {
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            // "HTTP_X_CSRFTOKEN": getCookie("csrftoken"),
        }
    }
} 


// function getCookie(cname: string): string {
//     const name = cname + "=";
//     const decodedCookie = decodeURIComponent(document.cookie);
//     const ca = decodedCookie.split(';');
//     for(let i = 0; i <ca.length; i++) {
//         let c = ca[i];
//         while (c.charAt(0) == ' ') {
//             c = c.substring(1);
//         }
//         if (c.indexOf(name) == 0) {
//             return c.substring(name.length, c.length);
//         }
//     }
//     return "";
// }

function getCookie(name: string): string {
    let cookieValue = "";
    if (document.cookie && document.cookie !== '') {
        console.log(document.cookie);
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


export function deserializeTopics(arr: any[]): Topic[] {
    const topics: Topic[] = [];
    for (const record of arr) {
        topics.push(deserializeTopic(record))
    }
    return topics;
}


export function deserializeTopic(obj: any): Topic {
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


export function serializeTopic(topic: Topic): any {
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


export function deserializeMorphs(arr: any[]): Morph[] {
    const morphs: Morph[] = [];
    for (const record of arr) {
        morphs.push(deserializeMorph(record));
    }
    return morphs;
}


export function deserializeMorph(obj: any): Morph {
    return {
        id: obj.id,
        name: obj.name,
        summary: obj.summary,
        icon: obj.icon,
        template: obj.json_data,
    }
}


export function serializeMorph(morph: Morph): any {
    return {
        id: morph.id,
        name: morph.name,
        summary: morph.summary,
        icon: morph.icon,
        json_data: morph.template,
    }
}
