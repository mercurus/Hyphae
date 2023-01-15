export default class Topic {
    id: number;
    name: string;
    icon?: string;
    jsonData: any;
    morphId: number;
    userId?: number;
    createdById?: number;
    createdDate: Date;

    constructor(json: any) {
        this.id = json.id;
        this.name = json.name;
        this.icon = json.icon;
        this.jsonData = json.jsonData;
        this.morphId = json.morphId;
        this.userId = json.userId;
        this.createdById = json.createdById;
        this.createdDate = json.createdDate;
    }
}