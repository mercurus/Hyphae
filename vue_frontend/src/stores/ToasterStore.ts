import { defineStore } from "pinia";

interface Toast {
    message: string;
    icon: string;
    colorClass: string;
    key: number;
}

const useStoreToaster = defineStore("ToasterStore", {
    state: () => {
        return {
            activeToast: [] as Array<Toast>,
        }
    },
    
    actions: {
        //better to use the composable useToaster instead of this
        addToast(message: string, icon: string, colorClass: string) {
            this.activeToast.push({
                message,
                icon,
                colorClass,
                key: Math.random(), //used only in v-for as the :key
            });
            setTimeout(() => { this.activeToast.shift(); }, 5000);
        },
    },
});
export default useStoreToaster;