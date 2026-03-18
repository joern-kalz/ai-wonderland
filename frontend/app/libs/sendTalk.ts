interface SendTalkRequest {
    sessionToken: string;
    message: string;
}

interface SendTalkResponse {
    message: string;
}

export async function sendTalk(
    { sessionToken, message }: SendTalkRequest
): Promise<SendTalkResponse> {
    // const response = await fetch('https://picsum.photos/seed/picsum/1024/1024', {
    //     method: 'POST',
    //     body: JSON.stringify({ message }),
    //     headers: {
    //         'x-session-token': `${sessionToken}`,
    //         'Content-Type': 'application/json'
    //     }
    // });

    // return response.json();

    await new Promise(r => setTimeout(r, 2000));
    return { message }
}