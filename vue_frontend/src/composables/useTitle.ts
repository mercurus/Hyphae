export default function useTitle(title: string) {
    (window as any).document.title = title;
}
