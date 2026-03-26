import { API_URL } from "./config";

interface SendTalkRequest {
    sessionToken: string;
    message: string;
}

interface SendTalkResponse {
    message: string;
    game_end: boolean;
}

export async function sendTalk(
    { sessionToken, message }: SendTalkRequest
): Promise<SendTalkResponse> {
    const response = await fetch(`${API_URL}/talk`, {
        method: 'POST',
        body: JSON.stringify({ message }),
        headers: {
            'x-session-token': `${sessionToken}`,
            'Content-Type': 'application/json'
        }
    });

    if (!response.ok) {
        throw new Error(`Failed to talk: ${response.statusText}`);
    }

    return response.json();
}