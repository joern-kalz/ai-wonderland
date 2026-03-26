import { API_URL } from "./config";

interface SendStartGameResponse {
    sessionToken: string;
}

export async function sendStartGame(): Promise<SendStartGameResponse> {
    const response = await fetch(`${API_URL}/start`, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        }
    });

    if (!response.ok) {
        throw new Error(`Failed to start game: ${response.statusText}`);
    }

    return response.json();
}