import useToasterStore from "@/stores/ToasterStore";

export default function useToaster() {
    const toasterStore = useToasterStore();

    function showSuccess(message: string) {
        toasterStore.addToast(message, "circle-check", "is-success");
    }

    function showInfo(message: string) {
        toasterStore.addToast(message, "circle-info", "is-info");
    }

    function showWarning(message: string) {
        toasterStore.addToast(message, "triangle-exclamation", "is-warning");
    }

    function showError(message: string) {
        toasterStore.addToast(message, "face-frown", "is-danger");
    }

    function showCustom(message: string, icon: string, colorClass: string) {
        toasterStore.addToast(message, icon, colorClass);
    }

    return {
        showSuccess,
        showInfo,
        showWarning,
        showError,
        showCustom
    }
}
