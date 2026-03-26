import { API_URL } from "./config";

interface SendTravelRequest {
    sessionToken: string;
    destination: string;
}

interface SendTravelResponse {
    type: 'success' | 'not_a_character_error';
}

export async function sendTravel(
    { sessionToken, destination }: SendTravelRequest
): Promise<SendTravelResponse> {
    const response = await fetch(`${API_URL}/talk`, {
        method: 'POST',
        body: JSON.stringify({ npc: destination }),
        headers: {
            'x-session-token': `${sessionToken}`,
            'Content-Type': 'application/json'
        }
    });

    if (response.status === 400) {
        return { type: 'not_a_character_error' };
    } else if (!response.ok) {
        throw new Error(`Failed to travel: ${response.statusText}`);
    }

    return { type: 'success' };
}