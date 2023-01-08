export default class Morph {
    id: number;
    name: string;
    icon: string;
    template: {
        fields: MorphField[];
    };

    constructor(json: any) {
        this.id = json.id;
        this.name = json.name;
        this.icon = json.icon;
        this.template = {
            fields: json.fields || [],
        };
    }
}

interface MorphField {
    name: string;
    dataType: string;
}