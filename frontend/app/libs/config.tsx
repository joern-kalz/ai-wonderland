export const API_URL = removeTrailingSlash(process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000");

function removeTrailingSlash(url: string): string {
    return url.endsWith("/") ? url.slice(0, -1) : url;
}