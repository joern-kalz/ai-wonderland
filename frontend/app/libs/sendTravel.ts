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
    const response = await fetch('https://picsum.photos/seed/picsum/1024/1024', {
        method: 'POST',
        body: JSON.stringify({ destination }),
        headers: {
            'x-session-token': `${sessionToken}`,
            'Content-Type': 'application/json'
        }
    });

    return response.json();
}