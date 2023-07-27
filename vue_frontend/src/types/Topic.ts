export default interface Topic {
    id: number;
    name: string;
    summary: string;
    icon: string | null;
    jsonData: any;
    morphId: number;
    userId: number | null;
    createdById: number | null;
    createdDate: Date;
}
