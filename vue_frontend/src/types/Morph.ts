export default interface Morph {
    id: number;
    name: string;
    summary: string;
    icon: string;
    template: {
        fields: MorphField[];
    };
}

interface MorphField {
    name: string;
    dataType: string;
}
