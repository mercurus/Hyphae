import { ref } from "vue";
import axios, { AxiosRequestConfig, AxiosError } from "axios";
import useToaster from "@/composables/useToaster";

type CallMethod = "get" | "post" | "put";

export default function useAPI() {
    const isLoading = ref(false);
    const csrfToken = (document.getElementById("csrftoken") as HTMLInputElement)?.value || "";

    async function call(
        method: CallMethod,
        url: string,
        options: Record<string, string | Record<string, string>> | null,
        params: Record<string, string> | null,
        data: Record<string, string> | FormData | null,
        callback: (r: any) => void,
        errorCallback?: (r: any) => void
    ) {
        const toaster = useToaster();
        const config = {
            method,
            url,
            params,
            data,
            responseType: "json",
            headers: { 
                "X-CSRFToken": csrfToken, //not necessary for GET but whatever
            },
        } as AxiosRequestConfig;
        if (typeof options == "object") Object.assign(config, options);

        try {
            isLoading.value = true;
            const response = await axios(config);
            callback(response);
        }
        catch (error) {
            console.log(error);
            const e = error as AxiosError;
            if (e.isAxiosError) toaster.showError(e.response?.status ? "Error code " + e.response.status : e.message);
            else toaster.showError("Error on request");
            if (errorCallback) errorCallback(error);
        }
        finally {
            isLoading.value = false;
        }
    }

    async function get(url: string, params: Record<string, string> | null, callback: (r: any) => void, errorCallback?: (r: any) => void) {
        call("get", url, null, null, null, callback, errorCallback);
    }

    async function post(url: string, data: Record<string, string> | FormData | null, callback: (r: any) => void, errorCallback?: (r: any) => void) {
        call("post", url, null, null, data, callback, errorCallback);
    }

    async function put(url: string, data: Record<string, string> | FormData | null, callback: (r: any) => void, errorCallback?: (r: any) => void) {
        call("put", url, null, null, data, callback, errorCallback);
    }

    async function postFile(url: string, file: File, callback: (r: any) => void, errorCallback?: (r: any) => void) {
        const formData = new FormData();
        formData.append("csv_file", file);
        const config = {
            headers: { 
                "Content-Type": "multipart/form-data",
                "X-CSRFToken": csrfToken,
            },
            responseType: "blob"
        };
        call("post", url, config, null, formData, callback, errorCallback);
    }

    return {
        call,
        get,
        post,
        put,
        postFile,
        isLoading
    }
}
