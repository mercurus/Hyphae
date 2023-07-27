import { ref, onMounted, onBeforeUnmount } from "vue";
import useToaster from "@/composables/useToaster";

//https://logaretm.com/blog/my-favorite-5-vuejs-composables/
export default function useFileUtilities() {
    const inputRef = ref<HTMLInputElement | null>(null);
    const files = ref<File[]>([]);

    onMounted(() => {
        const input = document.createElement("input");
        input.type = "file";
        input.hidden = true;
        document.body.appendChild(input);
        inputRef.value = input;
    });

    onBeforeUnmount(() => {
        inputRef.value?.remove();
    });

    function openFileDialog(extensions: string | string[] | null, multiple=false) {
        // skip if the input wasn"t mounted yet or was removed
        if (!inputRef.value) {
            files.value = [];
            return;
        }

        if (typeof extensions == "string") {
            inputRef.value.accept = "." + extensions;
        }
        else if (Array.isArray(extensions)) {
            inputRef.value.accept = extensions.map((ext) => `.${ext}`).join(",");
        }

        inputRef.value.multiple = multiple;
        inputRef.value.onchange = (event) => {
            const fileList = (event.target as HTMLInputElement).files;
            files.value = fileList ? Array.from(fileList) : [];
            // clear the event listener
            if (inputRef.value) inputRef.value.onchange = null;
        };
        inputRef.value.click();
    }

    function chosenFile() {
        if (files.value) return files.value[0];
        return null;
    }

    function chosenFiles() {
        if (files.value) return files.value;
        return null;
    }

    function downloadFile(response: any, filename="") {
        const toaster = useToaster();
        try {
            if (!filename) {
                const filenameHeader = (response.headers["content-disposition"] || "").match(/filename="(.*)"/);
                if (filenameHeader) filename = filenameHeader[1];
                else filename = "file.txt";
            }

            //https://stackoverflow.com/a/53230807
            const link = document.createElement("a");
            link.href = URL.createObjectURL(response.data);
            link.setAttribute("download", filename);
            document.body.appendChild(link);
            link.click();
            //clean up
            document.body.removeChild(link);
            URL.revokeObjectURL(link.href);
        }
        catch (error) {
            console.log(error);
            toaster.showError("Error on download");
        }
    }

    return {
        openFileDialog,
        chosenFile,
        chosenFiles,
        downloadFile
    }
}
