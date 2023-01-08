export default interface Topic {
    name: string;
    icon?: string;
    jsonData: any;
    morphId: number;
    userId?: number;
    createdById?: number;
    createdDate: Date;
}