interface SendStartGameResponse {
    sessionToken: string;
}

export async function sendStartGame(): Promise<SendStartGameResponse> {
    const response = await fetch('https://picsum.photos/seed/picsum/1024/1024', {
        method: 'POST',
    });

    return response.json();
}