import { API_URL } from "./config";

export async function sendGetNpcImage(sessionToken: string): Promise<Blob> {
    const response = await fetch(`${API_URL}/image`, {
        headers: {
            'x-session-token': `${sessionToken}`,
        }
    });

    if (!response.ok) {
        throw new Error(`Failed to get npc image: ${response.statusText}`);
    }

    return response.blob();
}